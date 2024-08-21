pip install awscli
s3_bucket="s3://mlops-research/mlflow/mlruns"
aws s3 sync ../../mlruns $s3_bucket