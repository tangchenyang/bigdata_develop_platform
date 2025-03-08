import logging


def init_logging():
    print(f"Initializing logging, level: INFO")
    # logging.basicConfig(
    #     format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    #     level=logging.INFO,
    #     datefmt="%Y-%m-%dT%H:%M:%S%z",
    # )
    # 设置 root logger 的格式
    root = logging.getLogger()
    formatter = logging.Formatter("[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)


init_logging()
