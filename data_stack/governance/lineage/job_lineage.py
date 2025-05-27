import logging
from typing import Dict, List

from data_stack.models.job.base_job import Job
from data_stack.utils.dag_helper import DAGHelper

# todo save to table or some where
_job_lineages: Dict[Job, List[Job]] = {}


def register_job_lineage(job: Job, upstream_jobs: List[Job]):

    _job_lineages[job] = upstream_jobs

    logging.info(f"Registered lineage for job {job.name}")

def get_all_job_lineages():
    return _job_lineages


def to_graph():
    lineages = get_all_job_lineages()
    dag_helper = DAGHelper()

    for job, upstream_jobs in lineages.items():
        dag_helper.add_node(str(job))
        for upstream_job in upstream_jobs:
            dag_helper.add_node(str(upstream_job))
            dag_helper.add_edge(str(upstream_job), str(job))
    logging.info(f"Built job lineage graph")
    return dag_helper.graph

def draw_lineages(path: str):
    DAGHelper(to_graph()).draw(path)
