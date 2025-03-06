# Carpenter: Job Scraper

Carpenter is a job scraping tool that extracts job listings from Jobrapido and Glassdoor. It allows users to search for job titles and export the results to CSV files. 

## Features

- Scrape job listings from Jobrapido and Glassdoor (at the moment).
- Export job listings to CSV files.
- Command-line interface for easy usage.

## Requirements

- Python 3.10
- `pip` for managing Python packages
- Chrome installed on your PC
- Chrome driver installed on your PC

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/devgabrielsborges/Carpenter.git
    cd Carpenter
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Download the Chrome driver from [here](https://googlechromelabs.github.io/chrome-for-testing/) and ensure it is in your system's PATH.

## Usage

Run the script from the command line with the following syntax:
```sh
python cli.py <search_term> <choice>
```

- `<search_term>`: The job title you want to search for.
- `<choice>`: The site you want to scrape jobs from. Options are `jobrapido` and `glassdoor`.

### Example

```sh
python cli.py "software engineer" jobrapido
```

This command will search for "software engineer" jobs on Jobrapido and export the results to a CSV file.

## Project Structure

- `cli.py`: The main script to run the job scraping functions.
- `jobrapido.py`: Module for scraping Jobrapido.
- `glassdoor.py`: Module for scraping Glassdoor.
- `commons.py`: Common functions used across the project, such as exporting jobs to CSV.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
