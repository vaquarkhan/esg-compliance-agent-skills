"""AWS CDK stack: ECS Fargate MCP servers, ALB, DynamoDB, S3, OpenSearch Serverless.

Multi-region deployment targets (deploy separate stacks per region):
  - eu-west-1      : EU CSRD / ESEF primary
  - us-east-1      : SEC climate / SFDR US operations
  - ap-south-1     : India DPDP localization
  - ap-southeast-1 : APAC supply-chain due diligence
  - me-south-1     : Saudi PDPL / Middle East workloads
"""

from __future__ import annotations

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_opensearchserverless as opensearchserverless,
    aws_s3 as s3,
)
from constructs import Construct

MCP_SERVICES = [
    {"name": "regulatory-db", "port": 8001},
    {"name": "emissions-factor", "port": 8002},
    {"name": "taxonomy-criteria", "port": 8003},
    {"name": "filing-submission", "port": 8004},
    {"name": "sanctions-screening", "port": 8005},
]


class EsgComplianceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, stack_suffix: str = "primary", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "EsgVpc", max_azs=2, nat_gateways=1)

        cluster = ecs.Cluster(self, "McpCluster", vpc=vpc, container_insights=True)

        audit_table = dynamodb.Table(
            self,
            "AuditLogTable",
            partition_key=dynamodb.Attribute(name="pk", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
            point_in_time_recovery=True,
        )

        audit_bucket = s3.Bucket(
            self,
            "AuditArchiveBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="GlacierDeepArchiveAfter1Year",
                    enabled=True,
                    transitions=[
                        s3.Transition(storage_class=s3.StorageClass.GLACIER, transition_after=Duration.days(90)),
                        s3.Transition(
                            storage_class=s3.StorageClass.DEEP_ARCHIVE,
                            transition_after=Duration.days(365),
                        ),
                    ],
                    expiration=Duration.days(365 * 8),
                )
            ],
        )

        collection = opensearchserverless.CfnCollection(
            self,
            "RegulatoryKnowledgeBase",
            name=f"esg-reg-kb-{stack_suffix}",
            type="VECTORSEARCH",
            description="Regulatory knowledge base for ESG MCP servers",
        )

        alb = elbv2.ApplicationLoadBalancer(
            self,
            "McpAlb",
            vpc=vpc,
            internet_facing=True,
        )
        listener = alb.add_listener("HttpListener", port=80, open=True)

        for idx, svc in enumerate(MCP_SERVICES):
            fargate = ecs_patterns.ApplicationLoadBalancedFargateService(
                self,
                f"McpService{svc['name'].replace('-', '').title()}",
                cluster=cluster,
                cpu=256,
                memory_limit_mib=512,
                desired_count=1,
                public_load_balancer=False,
                task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("python:3.11-slim"),
                    container_port=svc["port"],
                    environment={
                        "MCP_PORT": str(svc["port"]),
                        "MCP_HOST": "0.0.0.0",
                        "AUDIT_TABLE": audit_table.table_name,
                        "AUDIT_BUCKET": audit_bucket.bucket_name,
                    },
                ),
            )
            target_group = elbv2.ApplicationTargetGroup(
                self,
                f"Tg{idx}",
                vpc=vpc,
                port=svc["port"],
                targets=[fargate.service],
                health_check=elbv2.HealthCheck(path="/sse", healthy_http_codes="200-499"),
            )
            listener.add_action(
                f"Route{svc['name']}",
                priority=idx + 1,
                conditions=[elbv2.ListenerCondition.path_patterns([f"/{svc['name']}/*"])],
                action=elbv2.ListenerAction.forward([target_group]),
            )
            audit_table.grant_read_write_data(fargate.task_definition.task_role)
            audit_bucket.grant_read_write(fargate.task_definition.task_role)

        from aws_cdk import CfnOutput

        CfnOutput(self, "AlbDns", value=alb.load_balancer_dns_name)
        CfnOutput(self, "AuditTableName", value=audit_table.table_name)
        CfnOutput(self, "AuditBucketName", value=audit_bucket.bucket_name)
        CfnOutput(self, "OpenSearchCollection", value=collection.attr_arn)
