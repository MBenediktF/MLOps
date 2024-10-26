from mysql_helpers import init_table, insert_record
from mysql_helpers import get_records, update_record
from uuid import uuid4
from hashlib import sha256
from log_message import log_message, ERROR

# Create clients table
init_table(
    "clients",
    """
        id INT AUTO_INCREMENT PRIMARY KEY,
        uid VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        api_key_hash VARCHAR(255) NOT NULL,
        model_name VARCHAR(255) NOT NULL,
        model_version VARCHAR(255) NOT NULL,
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
            ("uid", "name", "api_key_hash", "model_name", "model_version"),
            (uid, name, api_key_hash, "", "")
        )
    except Exception as e:
        log_message(f"Could not create client: {e}", ERROR)
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
    log_message(f"Client: {client}")
    if not client:
        log_message("Unauthorzed")
        return False
    return True


def set_client_model(uid, model_name, model_version) -> int:
    return update_record(
        "clients",
        {"model_name": model_name, "model_version": model_version},
        f"uid='{uid}'"
    )


def get_client_model(uid) -> tuple:
    client = get_records("clients", f"uid='{uid}'")
    if not client:
        return None, None
    model = client[0][4]
    version = client[0][5]
    return model, version
