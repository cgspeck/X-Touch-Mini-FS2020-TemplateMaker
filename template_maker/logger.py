import logging


def get_logger() -> logging.Logger:
    return logging.getLogger("template-maker")


def setup_logger() -> logging.Logger:
    logger: logging.Logger = get_logger()
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
