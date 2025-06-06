import logging
from typing import List

from pyspark.sql import SparkSession

from data_stack.governance.quality.quality_checker import QualityChecker
from data_stack.models.data_asset.base_data_asset import DataAsset


class Job:
    name = None
    inputs: List[DataAsset] = None
    output: DataAsset = None

    spark: SparkSession = None

    def __init__(self):
        if self.name is None:
            self.name = self.__class__.__name__ # todo to snake

    def __str__(self):
        return f"JOB-{self.name}"

    def __repr__(self):
        return self.__str__()


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

        # for data_asset in self.inputs:
        #     QualityChecker(self.spark).check(data_asset)


    def after_run(self):
        logging.info(f"Do something before after running the job")
        QualityChecker(self.spark).check(self.output) # todo separate to a testing job from compute job to avoid compute job failure


