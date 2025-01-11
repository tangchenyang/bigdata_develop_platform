import logging
from typing import List

from data_stack.governance.quality import quality_checker
from data_stack.governance.quality.quality_checker import QualityChecker
from data_stack.models.data_asset.base_data_asset import DataAsset
from data_stack.models.data_asset.table.table import Table


class Job:
    name = None
    inputs: List[DataAsset] = None
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

        self.before_run()
        self.process()
        self.after_run()

    def before_run(self):
        logging.info(f"Do something before running the job")

        for data_asset in self.inputs:
            QualityChecker.check(data_asset)


    def after_run(self):
        logging.info(f"Do something before after running the job")

        QualityChecker.check(self.output)
