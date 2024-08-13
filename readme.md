# How to start the mlfluw ui

- Create a classic personal access token in your github developer settings (it only needs the read packages permission) and paste it to .env
- Run 'make setiup_mlflow_ui' to setup the docker container
- Add the aws key id and secrret and the bucket name to the .env file
- Run 'make start_mlflow_ui' to start the docker container
- Access the mlflow ui at localhost:4444
- Run 'make stop_mlflow_ui' to stop the docker container
- Run 'make 'remove_mlflow_ui' to delete the docker container and the image