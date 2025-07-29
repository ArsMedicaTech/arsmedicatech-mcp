include .env


run-mcp:
	.\.venv\Scripts\activate
	python lib/llm/mcp/mcp_server.py


local-encryption-key:
	@echo "Generating encryption key..."
	@python3 -c "import secrets, string; print('ENCRYPTION_KEY=' + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)))"



# Docker
auth:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(DOCKER_REGISTRY)

create-repos:
	aws ecr create-repository --repository-name $(MCP_SERVER_IMAGE) --region us-east-1 || true

docker-mcp:
	docker build --build-arg PORT=$(MCP_SERVER_PORT) -t $(DOCKER_REGISTRY)/$(MCP_SERVER_IMAGE):$(MCP_SERVER_VERSION) -f Dockerfile.mcp .
	docker push $(DOCKER_REGISTRY)/$(MCP_SERVER_IMAGE):$(MCP_SERVER_VERSION)
	kubectl rollout restart deployment $(MCP_SERVER_DEPLOYMENT) --namespace=$(NAMESPACE)

