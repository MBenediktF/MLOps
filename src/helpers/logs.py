import logging
import os
from dotenv import load_dotenv

load_dotenv()

INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR

filename = f"logs/{os.getenv('LOGFILE_NAME')}"

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


def log(message: str, level: int = INFO):
    logging.log(level, message)
