from helpers.logs import log, ERROR
from helpers.mysql import init_table, insert_record
from helpers.mysql import get_records, update_record, delete_record
from helpers.influx import count_records
from uuid import uuid4

# Create deployments table
init_table(
    "deployments",
    """
        id INT AUTO_INCREMENT PRIMARY KEY,
        uid VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        model_name VARCHAR(255) NOT NULL,
        model_version VARCHAR(255) NOT NULL,
        active BOOLEAN DEFAULT FALSE,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    )


def create_deployment(name: str, model_name: str, model_version: str) -> str:
    uid = str(uuid4())
    try:
        insert_record(
            "deployments",
            ("uid", "name", "model_name", "model_version", "active"),
            (uid, name, model_name, model_version, False)
        )
    except Exception as e:
        log(f"Could not create deployment: {e}", ERROR)
        return None
    return uid


def get_deployment(id: str) -> tuple:
    deployment = get_records("deployments", f"id='{id}'")
    if not deployment:
        log(f"Deployment with id {id} not found", ERROR)
        return None, None, None, None
    name = deployment[0][2]
    model = deployment[0][3]
    version = deployment[0][4]
    active = deployment[0][5]
    return name, model, version, active


def get_active_deployment() -> tuple:
    deployment = get_records("deployments", "active='1'")
    if not deployment:
        log("No active deployment found", ERROR)
        return None, None, None, None
    name = deployment[0][2]
    model = deployment[0][3]
    version = deployment[0][4]
    return name, model, version


def list_deployments() -> list:
    records = get_records("deployments", "")
    deployments = []
    for record in records:
        deployment = {
            "uid": record[1],
            "name": record[2],
            "model_name": record[3],
            "model_version": record[4],
            "records": count_records(record[2]),
            "active": record[5],
            "timestamp": record[6]
        }
        deployments.append(deployment)
    return deployments


def set_active_deployment(uid: str) -> bool:
    updated = update_record(
        "deployments",
        {"active": '1'},
        f"uid='{uid}'"
    )
    if not updated:
        return False
    updated = update_record(
        "deployments",
        {"active": '0'},
        f"uid!='{uid}'"
    )
    return True


def delete_deployment(uid: str) -> bool:
    deleted = delete_record(
        "deployents",
        f"uid='{uid}'"
    )
    return True if deleted else False
