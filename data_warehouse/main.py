import logging

from data_stack.governance.lineage import data_lineage
from data_stack.governance.lineage import job_lineage
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

    # check governance result
    logging.info("=" * 30 + " governance result " + "=" * 30)
    logging.info(f"Data qualities {QualityChecker.get_all_qualities()}")
    logging.info(f"Data Lineages: {data_lineage.get_all_data_asset_lineages()}")
    logging.info(f"Job Lineages: {job_lineage.get_all_job_lineages()}")
