import asyncio
import json
import re
import aiohttp
from bs4 import BeautifulSoup

from classes import Job


async def fetch_page(session, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


async def get_jobrapido_page(search: str, page: int) -> list:
    jobs = []
    url = f"https://br.jobrapido.com/Vagas-de-Emprego-para-{search}?p={page}"
    async with aiohttp.ClientSession() as session:
        html_body = await fetch_page(session, url)

        soup = BeautifulSoup(html_body, "html.parser")
        possible_jobs = soup.find_all("div", {"class": "result-item js-result-item"})

        for job_element in possible_jobs:
            jobs_str = job_element.attrs['data-advert']
            job_attributes = json.loads(jobs_str)

            job = Job(
                title=re.sub(re.compile(r'<.*?>'), '', job_attributes['title']),   # exclude tags
                company=job_attributes['company'],
                location=job_attributes['location'],
                link=job_attributes['openAdvertUrl'],
            )

            jobs.append(job)
    return jobs


async def get_jobrapido(search: str) -> list:
    tasks = []
    for page in range(1, 20):
        tasks.append(get_jobrapido_page(search, page))

    results = await asyncio.gather(*tasks)
    jobs = [job for sublist in results for job in sublist if job not in results]
    return jobs
