import logging


logging.basicConfig(
    filename='inference_pipeline.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def log_message(message: str, level: int = logging.INFO):
    logging.log(level, message)
