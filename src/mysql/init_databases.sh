#!/bin/bash
set -e

# Create databases if they do not exist
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<EOF
CREATE DATABASE IF NOT EXISTS \`${CONFIG_DATABASE}\`;
CREATE DATABASE IF NOT EXISTS \`${DAGSTER_DATABASE}\`;
CREATE DATABASE IF NOT EXISTS \`${MLFLOW_DATABASE}\`;

-- Create user if not exists and set proper privileges
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_USER_PASSWORD}';

-- Grant privileges on specific databases
GRANT ALL PRIVILEGES ON \`${CONFIG_DATABASE}\`.* TO '${MYSQL_USER}'@'%';
GRANT ALL PRIVILEGES ON \`${DAGSTER_DATABASE}\`.* TO '${MYSQL_USER}'@'%';
GRANT ALL PRIVILEGES ON \`${MLFLOW_DATABASE}\`.* TO '${MYSQL_USER}'@'%';

-- Apply the changes
FLUSH PRIVILEGES;
EOF


