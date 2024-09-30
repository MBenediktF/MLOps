import logging


INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR


logging.basicConfig(
    filename='inference_pipeline.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=INFO
)


def log_message(message: str, level: int = INFO):
    logging.log(level, message)
