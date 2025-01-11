import logging

from data_stack.models.job.base_job import Job
from data_warehouse.tables import tables


class DwdMoutai(Job):
    name = "dwd_moutai"

    inputs = [
        tables.ods_moutai
    ]
    output = tables.dwd_moutai

    def process(self):
        logging.info(f"Reading from {self.inputs}")
        logging.info(f"Transforming")
        logging.info(f"Save to {self.output}")

