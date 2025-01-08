import logging

from data_warehouse.workflows import registration
from data_warehouse.runner.job_runner import run_job


def init_logging():
    logging.basicConfig(
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )


if __name__ == '__main__':
    init_logging()
    registration.register_all()
    job_name = "dwd_moutai"

    run_job(job_name)
