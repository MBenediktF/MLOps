build_mlflow_ui_container:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@docker build -t mlflow_s3_sync_image -f mlflow/Dockerfile mlflow
	@docker save -o mlflow/mlflow_s3_sync_image.tar mlflow_s3_sync_image
	@docker rmi mlflow_s3_sync_image

start_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@if ! docker images --format "{{.Repository}}" | grep -q "^mlflow_s3_sync_image$$"; then \
		if [ -f mlflow/mlflow_s3_sync_image.tar ]; then \
			echo "Image mlflow_s3_sync_image not found. Loading image from mlflow_s3_sync_image.tar ..."; \
			sudo docker load -i mlflow/mlflow_s3_sync_image.tar; \
		else \
			echo "Image mlflow_s3_sync_image not found and mlflow_s3_sync_image.tar does not exist. Please build or export the image."; \
			exit 1; \
		fi \
	else \
		echo "Image mlflow_s3_sync_image exists."; \
	fi
	@if docker ps -a --format '{{.Names}}' | grep -w mlflow_ui > /dev/null; then \
		if docker ps --format '{{.Names}}' | grep -w mlflow_ui > /dev/null; then \
			echo "Container mlflow_ui is already running."; \
		else \
			echo "Starting existing container mlflow_ui..."; \
			docker start mlflow_ui; \
		fi \
	else \
		echo "Creating and starting a new container ..."; \
		docker run -d -p 4444:5000 --name mlflow_ui mlflow_s3_sync_image; \
	fi
	@echo "MLflow UI is running at http://localhost:4444"

stop_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@docker stop mlflow_ui

remove_mlflow_ui:
	@docker info > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker." && exit 1)
	@docker stop mlflow_ui || true
	@docker rm mlflow_ui || true
	@docker rmi mlflow_s3_sync_image || true
