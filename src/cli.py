from sys import argv, exit
import jobrapido, glassdoor, commons
import asyncio


'''

This script is used to run the job scraping functions from the jobrapido and glassdoor modules.
It receives a search term and a choice of which site to scrape jobs from.
The search term is the job title you want to search for.
The choice is the site you want to scrape jobs from. The options are "jobrapido" and "glassdoor".

Usage: python cli.py <search_term> <choice>

'''
if __name__ == "__main__":
    search_test = str(argv[1]).strip().lower() if len(argv) > 1 else None

    if search_test is None:
        print("You must provide a search term")
        exit(1)
    choice = argv[2].strip().lower() if len(argv) > 2 else None

    if choice == "jobrapido":
        jobs = asyncio.run(jobrapido.get_jobrapido(search_test))
        commons.export_jobs_to_excel("Jobrapido", search_test, jobs)
        print(f"Exported {len(jobs)} jobs to CSV in jobsData/Jobrapido/{search_test}.csv")
    elif choice == "glassdoor":
        commons.export_jobs_to_excel("Glassdoor", search_test,
        glassdoor.get_glassdoor(search_test.replace(" ", "-")))
        print(f"Exported jobs to CSV in jobsData/Glassdoor/{search_test}")
    else:
        print("Invalid choice")
        exit(1)
