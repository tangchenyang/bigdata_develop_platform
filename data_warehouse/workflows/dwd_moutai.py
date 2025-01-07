from data_warehouse.models.job.base import Job
from data_warehouse.workflows import tables


class DwdMoutai(Job):
    name = "DwdMoutai"

    input_tables = [
        tables.OdsTable
    ]
    output_table = tables.dwd_moutai

    def process(self):
        print(f"reading from {self.input_tables}")
        print(f"transforming")
        print(f"Save to {self.output_table}")

