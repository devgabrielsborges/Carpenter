import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from classes import Job
from commons import set_job_range


def extract_job_details(titles: list, locations: list, companies: list, index: int) -> (str, str, str):
    try:
        title = titles[index].text.replace("/", ", ")
        location = locations[index].text
        company = companies[index].text
        return title, location, company
    except IndexError:
        return None, None, None

def close_popup(wait):
    try:
        close_button = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'CloseButton')))
        close_button.click()
    except TimeoutException:
        pass

def get_glassdoor(search: str) -> list:
    jobs_list = []
    total_scraped_jobs = 0

    driver = uc.Chrome()
    driver.get(f"https://www.glassdoor.com.br/Vaga/brasil-{search}-vagas-SRCH_IL.0,6_IN36_KO7,21.htm")
    wait = WebDriverWait(driver, 15)

    job_quantity_text = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="left-column"]/div[1]/h1'))).text
    job_quantity = set_job_range(job_quantity_text)

    while total_scraped_jobs < job_quantity:
        titles = driver.find_elements(By.CLASS_NAME, 'JobCard_jobTitle___7I6y')
        jobs = driver.find_elements(By.CLASS_NAME, 'JobCard_jobCardWrapper__lyvNS')
        companies = driver.find_elements(By.CLASS_NAME, 'EmployerProfile_compactEmployerName__LE242')
        locations = driver.find_elements(By.CLASS_NAME, 'JobCard_location__rCz3x')

        for i in range(total_scraped_jobs, len(jobs)):
            jobs[i].click()

            if i == 1:
                close_popup(wait)

            title, location, company = extract_job_details(titles, locations, companies, i)

            if title is None:
                continue

            try:
                details_button = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'JobDetails_showMore___Le6L')))
                details_button.click()
                details = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="app-navigation"]/div[4]/div[2]/div[2]/div/div[1]')))
                _job = Job(title=title, company=company, location=location, description=details.text)
                jobs_list.append(_job)
            except TimeoutException as error:
                with open("logs.txt", "a") as logs:
                    logs.write(f"Error finding details: {error}\n")

            total_scraped_jobs += 1

        try:
            more_jobs = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="left-column"]/div[2]/div/button')))
            more_jobs.click()
        except StaleElementReferenceException:
            more_jobs = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="left-column"]/div[2]/div/button')))
            more_jobs.click()
        except TimeoutException:
            break

    driver.quit()
    return jobs_list
