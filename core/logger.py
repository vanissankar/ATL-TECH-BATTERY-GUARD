import logging
import os


LOG_FOLDER = "logs"
LOG_FILE = os.path.join(
    LOG_FOLDER,
    "app.log"
)


def setup_logger():

    if not os.path.exists(LOG_FOLDER):

        os.makedirs(LOG_FOLDER)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    logging.info(
        "Logger Started"
    )


def log_info(message):

    logging.info(message)


def log_error(message):

    logging.error(message)