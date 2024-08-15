# This is needed to make the env vars accessible to your python file when you want to exexute it locally

source .env
export BUCKET_NAME=$BUCKET_NAME
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY