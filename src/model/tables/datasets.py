from helpers.logs import log, ERROR
from helpers.mysql import init_table, insert_record
from helpers.mysql import get_records

# Create deployments table
init_table(
    "datasets",
    """
        id INT AUTO_INCREMENT PRIMARY KEY,
        uid VARCHAR(255) NOT NULL,
        measurements VARCHAR(255) NOT NULL,
        size VARCHAR(255) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    )


def store_dataset(uid: str, measurements: str, size: str) -> None:
    try:
        insert_record(
            "datasets",
            ("uid", "measurements", "size"),
            (uid, measurements, size)
        )
    except Exception as e:
        log(f"Could not store dataset: {e}", ERROR)
    return


def list_datasets() -> list:
    records = get_records("datasets", "")
    datasets = []
    for record in records:
        dataset = {
            "uid": record[1],
            "measurements": record[2],
            "size": record[3],
            "timestamp": record[4]
        }
        datasets.append(dataset)
    return datasets
