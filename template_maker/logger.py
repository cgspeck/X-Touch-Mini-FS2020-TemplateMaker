import logging


def get_logger() -> logging.Logger:
    return logging.getLogger("template-maker")


def setup_logger():
    logger = get_logger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
