import logging
import os

INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR

filename = "logs/model_services.log"

os.makedirs(os.path.dirname(filename), exist_ok=True)

# Initialize logfile if not already existing
if not os.path.exists(filename):
    with open(filename, mode='w') as file:
        file.write("")

logging.basicConfig(
    filename=filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=INFO
)


def log_message(message: str, level: int = INFO):
    logging.log(level, message)
