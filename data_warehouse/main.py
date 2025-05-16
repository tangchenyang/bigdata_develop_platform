import logging

def _setup_spark():
    from data_stack.models.job import base_job
    from data_warehouse.utils import spark_util

    base_job.Job.spark = spark_util.create_spark_session()


if __name__ == '__main__':

    from data_stack.governance.lineage import data_lineage
    from data_stack.governance.lineage import job_lineage
    from data_stack.governance.quality.quality_checker import QualityChecker
    from data_stack.runner.job_runner import run_job
    from data_warehouse import registration, DW_DIR

    _setup_spark()

    registration.register_all()
    run_job("ods_stock_info_s_d")
    run_job("ods_stock_market_s_d")
    run_job("dim_stock")
    run_job("dwd_stock_market_s_d")
    run_job("dws_stock_market_s_d")
    run_job("ads_stock_boundary_s_d")

    # check governance result
    logging.info("=" * 30 + " governance result " + "=" * 30)
    logging.info(f"Data qualities {QualityChecker.get_all_qualities()}")
    logging.info(f"Data Lineages: {data_lineage.get_all_data_asset_lineages()}")
    data_lineage.draw_lineages(f"{DW_DIR}/graph/data_asset_lineage.svg")
    logging.info(f"Job Lineages: {job_lineage.get_all_job_lineages()}")
    job_lineage.draw_lineages(f"{DW_DIR}/graph/job_lineage.svg")
