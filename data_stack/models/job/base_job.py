import logging
from typing import List

from data_stack.governance.quality.quality_checker import QualityChecker
from data_stack.models.data_asset.base_data_asset import DataAsset


class Job:
    name = None
    inputs: List[DataAsset] = None
    output: DataAsset = None

    def __init__(self):
        if self.name is None:
            self.name = self.__class__.__name__ # todo to snake

    def __str__(self):
        return f"[Job: {self.name}]"

    def __repr__(self):
        return f"[Job: {self.name}]"


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
        from data_stack.governance.lineage import data_lineage, job_lineage

        QualityChecker.check(self.output)
        data_lineage.register_data_asset_lineage(self.output, self.inputs)

        from data_stack.meta import job_meta
        upstream_jobs = [job_meta.get_job_by_output_data_asset(self.output) for data_asset in self.inputs]
        job_lineage.register_job_lineage(self, upstream_jobs)

