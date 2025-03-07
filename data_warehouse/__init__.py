import logging


def init_logging():
    print(f"Initializing logging, level: INFO")
    logging.basicConfig(
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    logging.root.setLevel("INFO") # todo global logger


init_logging()
