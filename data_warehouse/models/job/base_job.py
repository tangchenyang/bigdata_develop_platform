import logging

from data_warehouse.models.data_asset.base_data_asset import DataAsset


class Job:
    name = None
    inputs = None
    output: DataAsset = None

    def __init__(self):
        if self.name is None:
            self.name = self.__class__.__name__ # todo to snake

    def process(self):
        pass

    def run(self):
        logging.info(f"Running job {self.name}")
        logging.info(f"Inputs: {self.inputs}")
        logging.info(f"Output: {self.output}")
        self.process()

    def before_run(self):
        logging.info(f"Do something before running the job")

    def after_run(self):
        logging.info(f"Do something before after running the job")
        if True:
            logging.info(f"Checking data quality for {self.output.asset_type} {self.output.name}")

