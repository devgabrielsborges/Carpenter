import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# options = uc.ChromeOptions()
# options.headless = True

search = "FastAPI  "
driver = uc.Chrome()

driver.get(f"https://www.glassdoor.com.br/Vaga/brasil-{search}-vagas-SRCH_IL.0,6_IN36_KO7,17.htm")

job_quantity = driver.find_element(By.XPATH, '//*[@id="left-column"]/div[1]/h1')
jobs = driver.find_elements(By.CLASS_NAME, 'JobCard_jobCardWrapper__lyvNS')

jobs_list = [["Title", "Company", "Type / Location", "Description"]]
titles = driver.find_elements(By.CLASS_NAME, 'JobCard_jobTitle___7I6y')
companys = driver.find_elements(By.CLASS_NAME, 'EmployerProfile_compactEmployerName__LE242')
locations = driver.find_elements(By.CLASS_NAME, 'JobCard_location__rCz3x')

for k, job in enumerate(jobs):
    job.click()

    try:
        if driver.find_element(By.CLASS_NAME, 'CloseButton'):
            driver.find_element(By.CLASS_NAME, 'CloseButton').click()
    except Exception as error:
        with open("logs.txt", "w") as logs:
            logs.write(f"{error}\n")

    title = titles[k].text.replace("/", ", ")
    location = locations[k].text
    company = companys[k].text

    try:
        details_buttom = driver.find_element(By.CLASS_NAME, 'JobDetails_showMore___Le6L')
        details_buttom.click()
    except Exception as error:
        with open("logs.txt", "w") as logs:
            logs.write(f"{error}\n")

    details = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[4]/div[2]/div[2]/div/div[1]')
    jobs_list.append([title, company, location, details.text])

    driver.save_screenshot(f"jobs/{title}.png")

    archive_name = f"jobs/{title}.txt"
    with open(f"jobs/{title}.txt", "w") as archive:
        archive.write(f"{title}\n\n{location}\n\n{details.text}")

driver.quit()

df = pd.DataFrame(jobs_list)
df.to_csv(f"jobsData/glassdoor_{search}.csv", index=False)