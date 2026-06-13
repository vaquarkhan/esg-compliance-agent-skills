FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY mcp/ /app/mcp/
COPY knowledge_base/ /app/knowledge_base/
ENV PYTHONPATH=/app
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8005
EXPOSE 8005
CMD ["python", "mcp/sanctions-screening-server/server.py"]
