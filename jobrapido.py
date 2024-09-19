import requests
import json
from bs4 import BeautifulSoup
from classes import *

def get_jobrapido() -> list:
    jobs = []
    html_body = str(requests.get("https://br.jobrapido.com/?w=python").content).replace("\\", "")
    soup = BeautifulSoup(html_body, "html.parser")

    possible_jobs = soup.find_all("div", {"class": "result-item js-result-item"})

    for i in range(len(possible_jobs)):
        jobs_str = possible_jobs[i].attrs['data-advert']
        job_attributes = json.loads(jobs_str)

        job = Job(
            title=job_attributes['title'],
            company=job_attributes['company'],
            location=job_attributes['location'],
            link=job_attributes['openAdvertUrl'],
        )

        jobs.append (job)

    return jobs