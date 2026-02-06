import os
import re
from pathlib import Path

import pandas as pd

from classes import Job


def set_job_range(raw_job_quantity: str) -> int:
    raw_job_quantity = raw_job_quantity.replace(".", "").replace("/", "")
    num_pattern = re.compile(r"(\d+)")

    job_quantity = re.search(num_pattern, raw_job_quantity).group(1)

    return int(job_quantity)


def _sanitize_filename(raw_name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", raw_name).strip("_")
    return cleaned or "jobs"


def export_jobs_to_excel(site: str, search_name: str, jobs: [Job]):
    base_dir = Path("jobsData") / site
    base_dir.mkdir(parents=True, exist_ok=True)
    safe_name = _sanitize_filename(search_name)
    file_path = (base_dir / f"{safe_name}.xlsx").resolve()
    base_dir_resolved = base_dir.resolve()
    if not file_path.is_relative_to(base_dir_resolved):
        raise ValueError("Invalid search name for output file.")
    pd.DataFrame(jobs).to_excel(file_path, index=False)


def get_prompt_msg() -> str:
    if os.path.exists("prompet.txt"):
        with open("prompet.txt", "r", encoding="UTF8") as file:
            return str(file.read())
