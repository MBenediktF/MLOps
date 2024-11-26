from helpers.logs import Log, ERROR
from helpers.mysql import init_table, insert_record
from helpers.mysql import get_records, delete_record
from uuid import uuid4
from hashlib import sha256

log = Log()

# Create clients table
init_table(
    "clients",
    """
        id INT AUTO_INCREMENT PRIMARY KEY,
        uid VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        api_key_hash VARCHAR(255) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    )


def create_client(name: str) -> tuple:
    uid = str(uuid4())
    api_key = str(uuid4())
    api_key_hash = sha256(api_key.encode()).hexdigest()

    try:
        insert_record(
            "clients",
            ("uid", "name", "api_key_hash"),
            (uid, name, api_key_hash)
        )
    except Exception as e:
        log.log()(f"Could not create client: {e}", ERROR)
        return None, None
    return uid, api_key


def check_client_auth(uid: str, api_key: str) -> bool:
    try:
        api_key_hash = sha256(api_key.encode()).hexdigest()
    except Exception:
        return False

    # Check if client with api key exists
    client = get_records(
        "clients",
        f"uid='{uid}' AND api_key_hash='{api_key_hash}'"
        )
    return True if client else False


def list_clients() -> list:
    records = get_records("clients", "")
    clients = []
    for record in records:
        client = {
            "uid": record[1],
            "name": record[2],
            "timestamp": record[4]
        }
        clients.append(client)
    return clients


def delete_client(uid: str) -> bool:
    deleted = delete_record(
        "clients",
        f"uid='{uid}'"
    )
    return True if deleted else False
