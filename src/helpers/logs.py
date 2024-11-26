import logging
import os
from dotenv import load_dotenv

INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR

log_using_context = False


class Log:
    def __init__(self, context=False):
        self.context = context
        if not context:
            self.init_logging()
        else:
            context.log.info("Dagster Logging initialized")

    def init_logging(context=None):
        load_dotenv()
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

    def log(self, message: str, level: int = INFO):
        if not self.context:
            logging.log(level, message)
        else:
            if level == INFO:
                self.context.log.info(message)
            elif level == WARNING:
                self.context.log.warning(message)
            elif level == ERROR:
                self.context.log.error(message)