include .env
export $(shell sed 's/=.*//' .env)

start_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@echo "Logging in to GitHub Container Registry..."
	@echo $(GH_PERSONAL_ACCESS_TOKEN) | docker login ghcr.io -u USERNAME --password-stdin
	@echo "Downloading/Checking image..."
	@docker pull --quiet ghcr.io/bosch-devopsuplift/mlflow_ui_s3:main
	@if docker ps -a --format '{{.Names}}' | grep -w mlflow_ui > /dev/null; then \
		if docker ps --format '{{.Names}}' | grep -w mlflow_ui > /dev/null; then \
			echo "Container mlflow_ui is already running."; \
			exit 0; \
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
	@docker exec mlflow_ui /sync.sh

stop_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@if ! docker ps --format '{{.Names}}' | grep -w mlflow_ui > /dev/null; then \
		echo "Container mlflow_ui is not running."; \
		exit 1; \
	fi
	@echo "Syncing the data to S3..."
	@docker exec mlflow_ui /sync.sh
	@echo "Stopping container mlflow_ui..."
	@docker stop mlflow_ui
	@echo "Container mlflow_ui stopped."

remove_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@if docker ps --format '{{.Names}}' | grep -w mlflow_ui > /dev/null; then \
		echo "Container mlflow_ui is still running. Please stop the container before removing it."; \
		exit 1; \
	fi
	@echo "Removing container..."
	@docker rm mlflow_ui || true
	@echo "Removing image..."
	@docker rmi mlflow_ui_s3 || true
	@echo "Container and image removed."

download_datasets:
	@aws s3 sync s3://${BUCKET_NAME}/datasets datasets --exact-timestamps

download_dataset:
	@if [ -z "$(NAME)" ]; then \
		echo "Error: Please specify the dataset name or use download_datasets."; \
		exit 1; \
	fi
	@aws s3 ls s3://${BUCKET_NAME}/datasets/$(NAME)/ > /dev/null 2>&1 || { \
		echo "Error: The dataset '$(NAME)' does not exist in s3://${BUCKET_NAME}/datasets/"; \
		exit 1; \
	}
	@aws s3 sync s3://${BUCKET_NAME}/datasets/$(NAME) datasets/$(NAME) --exact-timestamps

upload_datasets:
	@aws s3 sync datasets s3://${BUCKET_NAME}/datasets --exact-timestamps

deploy_to_production:
	@if [ -z "$(NAME)" ]; then \
		echo "Error: Please specify the model name."; \
		exit 1; \
	fi
	@if [ -z "$(VERSION)" ]; then \
		echo "No version specified, using the newest one."; \
		VERSION="latest"; \
	fi; \
	curl -X POST \
		-H "Accept: application/vnd.github+json" \
		-H "Authorization: token ${GH_PERSONAL_ACCESS_TOKEN}" \
		https://api.github.com/repos/bosch-devopsuplift/sb.mlops_research/actions/workflows/deploy_to_production.yaml/dispatches \
  		-d "{\"ref\":\"main\", \"inputs\":{\"name\":\"${NAME}\",\"version\":\"$$VERSION\"}}"; \
	echo "Model deployment started. Please check the Actions tab in the repository for status and approval."
