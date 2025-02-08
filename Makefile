AWS_REGION=us-east-1
ECR_REGISTRY=019154908669.dkr.ecr.$(AWS_REGION).amazonaws.com
ECR_REPO=rikkeisoft-chatbot/backend
IMAGE_TAG=latest
ECS_CLUSTER=rikkeisoft-chatbot
ECS_SERVICE=rikkeisoft-chatbot-be
ECS_TASK=rikkei-chatbot

.PHONY: login build tag push update-ecs deploy

# Clear AWS environment variables to use .aws/credentials
clear-env:
	@set AWS_ACCESS_KEY_ID=
	@set AWS_SECRET_ACCESS_KEY=
	@set AWS_SESSION_TOKEN=
	@set AWS_SHARED_CREDENTIALS_FILE=%CD%\.aws\credentials

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

# Force ECS to use the latest pushed image
update-ecs:
	@aws ecs update-service --cluster $(ECS_CLUSTER) --service $(ECS_SERVICE) --task-definition $(ECS_TASK) --force-new-deployment --region $(AWS_REGION)

# Full deployment pipeline: login, build, tag, push, and update ECS
deploy: login build tag push update-ecs
	@echo Deployment completed!
