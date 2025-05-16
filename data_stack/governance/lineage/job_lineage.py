import logging
import os
from typing import Dict, List

from data_stack.models.job.base_job import Job

# todo save to table or some where
_job_lineages: Dict[Job, List[Job]] = {}


def register_job_lineage(job: Job, upstream_jobs: List[Job]):

    _job_lineages[job] = upstream_jobs

    logging.info(f"Registered lineage for job {job.name}")

def get_all_job_lineages():
    return _job_lineages

def draw_lineages(path: str):
    file_folder = os.path.dirname(path)
    file_name, file_format = os.path.basename(path).split(".")

    lineages = get_all_job_lineages()
    from data_stack.utils.dag_helper import DAGHelper
    dag_helper = DAGHelper(file_folder)

    for job, upstream_jobs in lineages.items():
        dag_helper.add_node(str(job))
        for upstream_job in upstream_jobs:
            dag_helper.add_node(str(upstream_job))
            dag_helper.add_edge(str(upstream_job), str(job))

    dag_helper.draw(output_file_name=file_name, output_file_format=file_format)
