include .env
export $(shell sed 's/=.*//' .env)

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

build_and_start_services:
	@docker-compose up -d --build

setup_and_start_services:
	@docker-compose up -d

start_services:
	@docker-compose start

stop_services:
	@docker-compose stop

edge_setup_venv:
	@source src/edge/venv/bin/activate

add_pythonpath:
	@export PYTHONPATH="${PYTHONPATH}:src"
