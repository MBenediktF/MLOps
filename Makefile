include .env
export $(shell sed 's/=.*//' .env)

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

dvc_pull_s3: 
	@dvc pull -r s3

dvc_commit_push_s3: dvc_config_s3_access
	@dvc commit datasets
	@dvc push -r s3	

pytest_run:
	@python -m pytest -v

launch_inference_api:
	@bash bash/launch_inference_api.sh

build_inference_api_docker:
	@docker build -f src/inference/Dockerfile -t inference_api .

run_inference_api_docker:
	@docker run -p 5001:5000 inference_api

build_mlflow_ui_docker:
	@docker build -f src/mlflow/Dockerfile -t mlflow_ui .

backup_docker_volumes:
	@bash bash/backup_docker_volumes.sh

restore_docker_volumes:
	@bash bash/restore_docker_volumes.sh

setup_and_start_services:
	@docker-compose up -d

start_services:
	@docker-compose start

stop_services:
	@docker-compose stop
