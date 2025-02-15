AWS_REGION=ap-southeast-2
ECR_REGISTRY=590183769116.dkr.ecr.$(AWS_REGION).amazonaws.com
ECR_REPO_PUBLIC=v7s8u3o1
# ECR_REPO=rikkeisoft-chatbot/backend
ECR_REPO=rikkeigpt/backend
IMAGE_TAG=latest
ECS_CLUSTER=rikkeigpt-cluster
ECS_SERVICE=rikkeigpt-service

.PHONY: clear-env load-creds login login-public build tag push update-ecs deploy

# Clear AWS environment variables to use .aws/credentials
clear-env:
	@echo Clearing AWS environment variables...
	@set AWS_ACCESS_KEY_ID=
	@set AWS_SECRET_ACCESS_KEY=
	@set AWS_SESSION_TOKEN=

load-creds:
	@echo Loading AWS credentials...
	@set AWS_SHARED_CREDENTIALS_FILE=%CD%\.aws\credentials
	@echo %AWS_SHARED_CREDENTIALS_FILE%
	@aws sts get-caller-identity

# Authenticate Docker to AWS ECR
# If using ECR public, we need to delete `"credsStore": "desktop",` in `~/.docker/config.json` to use this command
login: clear-env load-creds
	@aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_REGISTRY)
# @aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/$(ECR_REPO_PUBLIC)

# Build Docker image
build:
	@docker build -t $(ECR_REPO) .

# Tag Docker image
tag:
	@docker tag $(ECR_REPO):$(IMAGE_TAG) $(ECR_REGISTRY)/$(ECR_REPO):$(IMAGE_TAG)
# @docker tag $(ECR_REPO):$(IMAGE_TAG) public.ecr.aws/$(ECR_REPO_PUBLIC)/$(ECR_REPO):$(IMAGE_TAG)

# Push Docker image to ECR
push:
	@docker push $(ECR_REGISTRY)/$(ECR_REPO):$(IMAGE_TAG)
# @docker push public.ecr.aws/$(ECR_REPO_PUBLIC)/$(ECR_REPO):$(IMAGE_TAG)

# Force ECS to use the latest pushed image
serve:
	@aws ecs update-service --cluster $(ECS_CLUSTER) --service $(ECS_SERVICE) --force-new-deployment

# Full deployment pipeline: login, build, tag, push, serve
deploy: login build tag push
	@echo Deployment completed!
