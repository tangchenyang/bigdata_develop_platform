from typing import Union

from data_stack.models.job.base_job import Job
from data_stack.meta.job_meta import registered_jobs


def run_job(job: Union[Job, str]):
    if isinstance(job, str):
        if job not in registered_jobs:
            raise ValueError(f"Job {job} not registered")
        job = registered_jobs.get(job)

    job.run()
