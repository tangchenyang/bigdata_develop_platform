import logging
from typing import Dict, List

from data_stack.models.job.base_job import Job

registered_jobs: Dict[str, Job] = {}


def register_job(job: Job):
    if job.name in registered_jobs:
        raise ValueError(f"Job {job.name} already registered")
    registered_jobs[job.name] = job

    logging.info(f"Registered job {job.name}")


def register_jobs(jobs: List[Job]):
    for job in jobs:
        register_job(job)
