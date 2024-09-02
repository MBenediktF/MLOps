include .env
export $(shell sed 's/=.*//' .env)

setup_mlflow_ui:
	@docker pull --quiet ghcr.io/bosch-devopsuplift/mlflow_ui_s3:main
	@docker run -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) -e BUCKET_NAME=$(BUCKET_NAME)  -d -p 4444:5000 --name mlflow_ui ghcr.io/bosch-devopsuplift/mlflow_ui_s3:main; \

start_mlflow_ui:
	@docker start mlflow_ui;

sync_mlflow_ui:
	@docker exec mlflow_ui /sync.sh

stop_mlflow_ui: sync_mlflow_ui
	@docker stop mlflow_ui

remove_mlflow_ui:
	@docker rm mlflow_ui || true
	@docker rmi mlflow_ui_s3 || true

download_datasets:
	@aws s3 sync s3://${BUCKET_NAME}/datasets datasets --exact-timestamps

download_dataset:
	@aws s3 sync s3://${BUCKET_NAME}/datasets/$(NAME) datasets/$(NAME) --exact-timestamps

upload_datasets:
	@aws s3 sync datasets s3://${BUCKET_NAME}/datasets --exact-timestamps

start_prod_deployment_workflow:
	curl -X POST \
		-H "Accept: application/vnd.github+json" \
		-H "Authorization: token ${GH_PERSONAL_ACCESS_TOKEN}" \
		https://api.github.com/repos/bosch-devopsuplift/sb.mlops_research/actions/workflows/deploy_to_production.yaml/dispatches \
  		-d "{\"ref\":\"main\", \"inputs\":{\"name\":\"${NAME}\",\"version\":\"$$VERSION\"}}"; \

start_dev_deployment_workflow:
	curl -X POST \
		-H "Accept: application/vnd.github+json" \
		-H "Authorization: token ${GH_PERSONAL_ACCESS_TOKEN}" \
		https://api.github.com/repos/bosch-devopsuplift/sb.mlops_research/actions/workflows/deploy_to_development.yaml/dispatches \
  		-d "{\"ref\":\"main\", \"inputs\":{\"name\":\"${NAME}\",\"version\":\"$$VERSION\"}}"; \

dvc_list_remotes:
	@dvc remote list

dvc_add_remote_s3:
	@dvc remote add -d s3 s3://$(BUCKET_NAME)/datasets
	@dvc remote default s3

dvc_config_s3_access:
	@dvc remote modify --local s3 access_key_id $(AWS_ACCESS_KEY_ID)
	@dvc remote modify --local s3 secret_access_key $(AWS_SECRET_ACCESS_KEY)

dvc_push_s3: dvc_config_s3_access
	@dvc push -r s3	

