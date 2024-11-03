import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from classes import Job
from commons import set_job_range

class Glassdoor:
    @staticmethod
    def _set_driver():
        driver = uc.Chrome()

        return driver


    @staticmethod
    def _set_wait(driver: object) -> object:
        wait = WebDriverWait(driver, 15)

        return wait


    @staticmethod
    def extract_job_details(titles: list, locations: list, companies: list, index: int) -> (str, str, str):
        try:
            title = titles[index].text.replace("/", ", ")
            location = locations[index].text
            company = companies[index].text
            return title, location, company
        except IndexError:
            pass


    def __init__(self, search: str, *location: str | None):
        self.driver = self._set_driver()
        self.wait = self._set_wait(self.driver)
        self.search = search
        self.location = location
        self.job_quantity = 0
        self.jobs_list = []


    def get_home_page(self):
        # This URL is to avoid login popups. Do not change it.
        self.driver.get(f"https://www.glassdoor.com.br/Vaga/brasil-java-vagas-SRCH_IL.0,6_IN36_KO7,11.htm")


    def home_search(self):
        search_input = self.wait.until(ec.presence_of_element_located((By.ID, "searchBar-jobTitle")))
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.DELETE)

        self.driver.implicitly_wait(5)

        # Search for the job title
        search_input.send_keys(self.search)

        if self.location:
            location_input = self.wait.until((ec.presence_of_element_located((By.ID, "searchBar-location"))))

            location_input.send_keys(Keys.CONTROL + "a")
            location_input.send_keys(Keys.DELETE)

            location_input.send_keys(self.location)
            location_input.send_keys("\n")

        search_input.send_keys("\n")   # Enter

    def setup_search(self):
        self.get_home_page()
        self.home_search()
        self.get_job_range()

    def get_job_range(self):
        job_quantity_text = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="left-column"]/div[1]/h1'))).text
        job_quantity = set_job_range(job_quantity_text)

        self.job_quantity = job_quantity

    def get_glassdoor_search(self):
        total_scraped_jobs = 0
        self.setup_search()

        while total_scraped_jobs < self.job_quantity:
            titles = self.driver.find_elements(By.CLASS_NAME, 'JobCard_jobTitle___7I6y')
            jobs = self.driver.find_elements(By.CLASS_NAME, 'JobCard_jobCardWrapper__lyvNS')
            companies = self.driver.find_elements(By.CLASS_NAME, 'EmployerProfile_compactEmployerName__LE242')
            locations = self.driver.find_elements(By.CLASS_NAME, 'JobCard_location__rCz3x')

            for i in range(total_scraped_jobs, len(jobs)):
                self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'JobCard_jobCardWrapper__lyvNS')))
                jobs[i].click()

                if i == 1:
                    self.close_popup()

                title, location, company = self.extract_job_details(titles, locations, companies, i)

                if title is None:
                    continue

                try:
                    details_button = self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'JobDetails_showMore___Le6L')))
                    details_button.click()
                    details = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="app-navigation"]/div[4]/div[2]/div[2]/div/div[1]')))
                    _job = Job(title=title, company=company, location=location, description=details.text)
                    self.jobs_list.append(_job)
                except TimeoutException as error:
                    with open("logs.txt", "a") as logs:
                        logs.write(f"Error finding details: {error}\n")

                total_scraped_jobs += 1

            try:
                more_jobs = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="left-column"]/div[2]/div/button')))
                more_jobs.click()
            except StaleElementReferenceException:
                more_jobs = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="left-column"]/div[2]/div/button')))
                more_jobs.click()
            except TimeoutException:
                break


    def close_popup(self):
        try:
            close_button = self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'CloseButton')))
            close_button.click()
        except TimeoutException:
            pass

    def quit_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    search_term = "estágio python"
    location = "recife"
    search_obj = Glassdoor(search_term)
    search_obj.get_glassdoor_search()
    search_obj.quit_driver()
    print(f"Exported jobs to CSV in jobsData/Glassdoor/{search_term}")
