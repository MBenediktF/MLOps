docker run --rm -v sbmlops_research_grafana_data:/data -v $(pwd)/backup:/backup busybox tar czf /backup/grafana_data_backup.tar.gz -C /data .
docker run --rm -v sbmlops_research_log_data:/data -v $(pwd)/backup:/backup busybox tar czf /backup/log_data_backup.tar.gz -C /data .
docker run --rm -v sbmlops_research_minio_data:/data -v $(pwd)/backup:/backup busybox tar czf /backup/minio_data_backup.tar.gz -C /data .
docker run --rm -v sbmlops_research_mysql_data:/data -v $(pwd)/backup:/backup busybox tar czf /backup/mysql_data_backup.tar.gz -C /data .
docker run --rm -v sbmlops_research_influxdb_data:/data -v $(pwd)/backup:/backup busybox tar czf /backup/influxdb_data_backup.tar.gz -C /data .
docker run --rm -v sbmlops_research_influxdb_config:/data -v $(pwd)/backup:/backup busybox tar czf /backup/influxdb_config_backup.tar.gz -C /data .
