# Sandbox to implement MLOps practices

## How to start the mlflow ui

- Create a classic personal access token in your github developer settings (it only needs the read packages permission) and paste it to .env
- Add the aws key id and secrret and the bucket name to the .env file
- Run 'make start_mlflow_ui' to init and start the docker container
- Run 'sync_mlflow_ui' to sync your local changes with the database. Deletions of any kind are disabled.
- Access the mlflow ui at localhost:4444
- Run 'make stop_mlflow_ui' to stop the docker container
- Run 'make 'remove_mlflow_ui' to delete the docker container and the image

## How to manage raw datasets

- Datasets are stored in the folder `datasets`, which is not synced with github, but stored in s3 instead
- To download all existing datasets, use `make download_datasets`
- To download a specific dataset use `make download_dataset NAME=<dataset_name>`
- To upload a new dataset to s3, add it to the `datasets`folder and use `make upload_datasets`
- This feature is only for storing raw data. Procecced datasets are stored as artifacts and can be accessed using the mlflow ui

## How to deploy a model

- This is not finished yet!
- Your github token must be configured to allow repo and workflow access
- Run `make start_mnodel_deployment`to start the workflow
- Check the workflow status in github action for approval
