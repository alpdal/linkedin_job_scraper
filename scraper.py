from selenium import webdriver 
from parameters import username, password, position, location, page_count, file_name
from bs4 import BeautifulSoup
from random import random
import time
import csv
import parameters

browser = webdriver.Firefox()
random_time = 4 + (random() * 5)

def linkedin_log_in():
	#open linkedin
	browser.get("https://www.linkedin.com")
	time.sleep(random_time)

	# log in page
	# "Sign in" button => Right click => Inspect => Right click to selected HTML code => Copy => Copy XPath = /html/body/nav/a[3]
	log_in = browser.find_element_by_xpath("/html/body/nav/a[3]")
	log_in.click()
	time.sleep(random_time)

	# log in info
	username = browser.find_element_by_xpath("//*[@id=\"username\"]")
	password = browser.find_element_by_xpath("//*[@id=\"password\"]")

	username.send_keys(parameters.username)
	password.send_keys(parameters.password)

	# sign in button
	sign_in = browser.find_element_by_xpath("//*[@id=\"app__container\"]/main/div/form/div[3]/button")
	sign_in.click()
	time.sleep(random_time)

def collect_url(position, location, page_count):
	urls = []
	# visit google
	browser.get("https://www.google.com")
	time.sleep(random_time) 

	# search jobs from google 
	search = browser.find_element_by_name("q")
	query = "site:linkedin.com/jobs/view AND \"{}\" AND \"{}\" AND \"Apply\" AND \"Posted\"".format(position, location)
	search.send_keys(query)
	search.send_keys(u'\ue007')
	time.sleep(random_time)
	try:
		for page in range(page_count):
			linkedin_urls = browser.find_elements_by_css_selector("div.r")

			for url in linkedin_urls:
				url_href = url.find_element_by_tag_name("a").get_attribute("href")
				urls.append(url_href)

			if page + 1 < page_count:
				next_button = browser.find_element_by_xpath("//*[@id=\"pnnext\"]/span[2]")
				next_button.click()

			time.sleep(random_time)
	except: 
		input("Catched by Google Captcha\nTo continue, pass Google Captcha manually and press any key")
		for page in range(page_count):
			linkedin_urls = browser.find_elements_by_css_selector("div.r")

			for url in linkedin_urls:
				url_href = url.find_element_by_tag_name("a").get_attribute("href")
				urls.append(url_href)

			if page + 1 < page_count:
				next_button = browser.find_element_by_xpath("//*[@id=\"pnnext\"]/span[2]")
				next_button.click()

			time.sleep(random_time)

	return urls 

def page_parser(url):
	skills = []
	browser.get(url)
	time.sleep(random_time)
	content = browser.page_source
	parser = BeautifulSoup(content, "html.parser")

	h1 = parser.find_all("h1", class_="jobs-top-card__job-title t-24")
	post_header = h1[0].getText()

	a = parser.find_all("a", class_="jobs-top-card__company-url ember-view")
	company = a[0].getText()
	company = company.strip()
	company = company.strip("\n")

	span = parser.find_all("span", class_="jobs-top-card__bullet")
	location = span[0].getText()
	location = location.strip()
	location = location.strip("\n")

	ul = parser.find_all("ul", class_="jobs-ppc-criteria__list--skills")
	skill_list = ul[0].find_all("span", class_="jobs-ppc-criteria__value t-14 t-black t-normal ml2 block")

	for skill in skill_list:
		skill = skill.getText()
		skill = skill.strip().strip("\n")
		skills.append(skill)

	details = [post_header, company, location]
	details.extend(skills)

	return details

# log in linkedin
linkedin_log_in()

# collect_urls
urls = collect_url(position, location, page_count)

# collect job details
job_details = []

for url in urls:
	if "linkedin.com" in url:
		try:
			job_info = page_parser(url)
			job_details.append(job_info)
			#writer.writerow(job_info)
		except:
			pass


with open(file_name, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(job_details)

# wait before close
time.sleep(6)
browser.close()

