import logging

if __name__ == '__main__':

    from data_stack.governance.lineage import data_lineage
    from data_stack.governance.lineage import job_lineage
    from data_stack.governance.quality.quality_checker import QualityChecker
    from data_stack.runner.job_runner import run_job
    from data_warehouse import registration

    registration.register_all()
    run_job("ods_stock_info_s_d")
    run_job("ods_stock_market_s_d")
    run_job("dwd_stock_market_s_d")

    # check governance result
    logging.info("=" * 30 + " governance result " + "=" * 30)
    logging.info(f"Data qualities {QualityChecker.get_all_qualities()}")
    logging.info(f"Data Lineages: {data_lineage.get_all_data_asset_lineages()}")
    logging.info(f"Job Lineages: {job_lineage.get_all_job_lineages()}")
