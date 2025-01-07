from data_warehouse.models.job.base import Job
from data_warehouse.workflows import jobs


def init_jobs():
    jobs_classes = Job.__subclasses__()
    jobs_instances = [jobs_class() for jobs_class in jobs_classes]
    return jobs_instances

def run_job():
    jobs_instances = init_jobs()
    for job in jobs_instances:
        job.execute()


if __name__ == '__main__':
    run_job()
    # print(Job.__subclasses__())
