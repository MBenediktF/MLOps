include .env

setup_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@echo "Logging in to GitHub Container Registry..."
	@echo $(GHCR_PERSONAL_ACCESS_TOKEN) | docker login ghcr.io -u USERNAME --password-stdin
	@echo "Grabbing the container package..."
	@docker pull ghcr.io/bosch-devopsuplift/mlflow_ui_s3:main

start_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@if docker ps -a --format '{{.Names}}' | grep -w mlflow_ui > /dev/null; then \
		if docker ps --format '{{.Names}}' | grep -w mlflow_ui > /dev/null; then \
			echo "Container mlflow_ui is already running."; \
		else \
			echo "Starting existing container mlflow_ui..."; \
			docker start mlflow_ui; \
		fi \
	else \
		echo "Creating and starting a new container ..."; \
		docker run -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) -e BUCKET_NAME=$(BUCKET_NAME)  -d -p 4444:5000 --name mlflow_ui ghcr.io/bosch-devopsuplift/mlflow_ui_s3:main; \
	fi
	@echo "MLflow UI is running at http://localhost:4444"

sync_mlflow_ui:
	@docker exec mlflow_ui ./sync.sh

stop_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@echo "Syncing the data to S3..."
	@docker exec mlflow_ui ./sync.sh
	@echo "Stopping container mlflow_ui..."
	@docker stop mlflow_ui
	@echo "Container mlflow_ui stopped."

remove_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@echo "Stopping container if running..."
	@docker stop mlflow_ui || true
	@echo "Removing container..."
	@docker rm mlflow_ui || true
	@echo "Removing image..."
	@docker rmi mlflow_ui_s3 || true
	@echo "Container and image removed."
