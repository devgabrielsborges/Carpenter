import requests
import json
from bs4 import BeautifulSoup
from classes import *
from commons import export_jobs_to_csv


def get_jobrapido(search: str) -> list:
    jobs = []

    for index in range(1, 30):
        html_body = str(
            requests.get(f"https://br.jobrapido.com/Vagas-de-Emprego-para-{search}?p={index}").content
        ).replace("\\", "")

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

            jobs.append(job)

    return jobs

if __name__ == "__main__":
    search_test = "Flask"
    export_jobs_to_csv(search_test, get_jobrapido(search_test))