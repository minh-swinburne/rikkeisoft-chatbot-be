AWS_REGION=us-east-1
ECR_REGISTRY=019154908669.dkr.ecr.$(AWS_REGION).amazonaws.com
ECR_REPO=rikkeisoft-chatbot/backend
IMAGE_TAG=latest

.PHONY: login build tag push deploy

# Clear AWS environment variables to use .aws/credentials
clear-env:
	@unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN

# Authenticate Docker to AWS ECR
login: clear-env
	@aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_REGISTRY)

# Build Docker image
build:
	@docker build -t $(ECR_REPO) .

# Tag Docker image
tag:
	@docker tag $(ECR_REPO):$(IMAGE_TAG) $(ECR_REGISTRY)/$(ECR_REPO):$(IMAGE_TAG)

# Push Docker image to ECR
push:
	@docker push $(ECR_REGISTRY)/$(ECR_REPO):$(IMAGE_TAG)

# Full deployment pipeline: login, build, tag, and push
deploy: login build tag push
	@echo "Deployment completed!"
