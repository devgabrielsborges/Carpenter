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
    print(len(argv))
    if len(argv) > 3:
        search_term = str(argv[1]).strip().lower()
        location = str(argv[2]).strip().lower()
        choice = argv[3].strip().lower()
    elif len(argv) > 2:
        search_term = str(argv[1]).strip().lower()
        location = None
        choice = argv[2].strip().lower()

    if search_term is None:
        print("You must provide a search term")
        exit(1)


    if choice == "jobrapido":
        jobs = asyncio.run(jobrapido.get_jobrapido(search_term))
        commons.export_jobs_to_csv("Jobrapido", search_term, jobs)
        print(f"Exported {len(jobs)} jobs to CSV in jobsData/Jobrapido/{search_term}.csv")
    elif choice == "glassdoor":
        if len(argv) <= 4:
            search_obj = glassdoor.Glassdoor(search_term, location)
        search_obj.get_glassdoor_search()
        search_obj.quit_driver()

        commons.export_jobs_to_csv("Glassdoor", search_term.replace(" ", "_"), search_obj.jobs_list)
        print(f"Exported jobs to CSV in jobsData/Glassdoor/{search_term}")
    else:
        print("Invalid choice")
        exit(1)
