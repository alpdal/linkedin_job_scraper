# linkedin_scraper

> Linkedin Job Post Scraper. 

Scrapes job title, location, company and needed skills via selenium. 

It can be used for data analysis of job posts with specific title and location. 
It can be easily converted to a job application bot. (not recommended)

Current scraped details may be enhanced, pull requests are welcomed. 

## Prerequisites

- selenium
- bs4
- firefox and geckodriver
- parameters.py

### parameters.py


```python 
# linkedin info
username = "username@mail.com"
password = "password"

# search_parameters
position = "engineer"
location = "istanbul"

# how many page will be searched via google (1 page returns 10 job post) 
page_count = 3

# results file
file_name = 'results_file.csv'
```
