docker run --rm -v sbmlops_research_grafana_data:/data -v $(pwd)/backup:/backup busybox tar xzf /backup/grafana_data_backup.tar.gz -C /data
docker run --rm -v sbmlops_research_log_data:/data -v $(pwd)/backup:/backup busybox tar xzf /backup/log_data_backup.tar.gz -C /data
docker run --rm -v sbmlops_research_minio_data:/data -v $(pwd)/backup:/backup busybox tar xzf /backup/minio_data_backup.tar.gz -C /data
docker run --rm -v sbmlops_research_mysql_data:/data -v $(pwd)/backup:/backup busybox tar xzf /backup/mysql_data_backup.tar.gz -C /data
docker run --rm -v sbmlops_research_influxdb_data:/data -v $(pwd)/backup:/backup busybox tar xzf /backup/influxdb_data_backup.tar.gz -C /data
docker run --rm -v sbmlops_research_influxdb_config:/data -v $(pwd)/backup:/backup busybox tar xzf /backup/influxdb_config_backup.tar.gz -C /data