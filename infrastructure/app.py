#!/usr/bin/env python3
"""AWS CDK app entry for ESG compliance MCP infrastructure."""

import aws_cdk as cdk
from esg_compliance_stack import EsgComplianceStack

app = cdk.App()

# Primary stack — replicate per region for multi-region deployment
EsgComplianceStack(
    app,
    "EsgComplianceStack-EU",
    env=cdk.Environment(account="123456789012", region="eu-west-1"),
    stack_suffix="eu-west-1",
)

app.synth()
