import pandas as pd
import os
import re
from classes import Job


def set_job_range(raw_job_quantity: str) -> int:
    raw_job_quantity = raw_job_quantity.replace(".", "").replace("/", "")
    num_pattern = re.compile(r"(\d+)")

    job_quantity = re.search(num_pattern, raw_job_quantity).group(1)

    return int(job_quantity)


def export_jobs_to_excel(site: str, search_name: str, jobs: [Job]):
    if not os.path.exists(site):
        os.makedirs(f"jobsData/{site}", exist_ok=True)
        pd.DataFrame(jobs).to_excel(f"jobsData/{site}/{str(search_name).strip()}.xlsx", index=False)
