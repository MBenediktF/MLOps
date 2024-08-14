# How to start the mlflow ui

- Create a classic personal access token in your github developer settings (it only needs the read packages permission) and paste it to .env
- Add the aws key id and secrret and the bucket name to the .env file
- Run 'make start_mlflow_ui' to init and start the docker container
- Run 'sync_mlflow_ui' to sync your local changes with the database. Deletions of any kind are disabled.
- Access the mlflow ui at localhost:4444
- Run 'make stop_mlflow_ui' to stop the docker container
- Run 'make 'remove_mlflow_ui' to delete the docker container and the image