import logging
from typing import Dict, List

from data_stack.models.job.base_job import Job

# todo save to table or some where
_job_lineages: Dict[Job, List[Job]] = {}


def register_job_lineage(job: Job, upstream_jobs: List[Job]):

    _job_lineages[job] = upstream_jobs
    logging.info(f"Registered lineage for job {job.name}")

def get_all_job_lineages():
    return _job_lineages
