import logging

from data_stack.governance.quality.quality_checker import QualityChecker
from data_stack.runner.job_runner import run_job
from data_warehouse import registration


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

    logging.info(f"{QualityChecker.data_asset_qualities}")
