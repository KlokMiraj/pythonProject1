import random
from urllib import request
from bs4 import BeautifulSoup
from itertools import cycle
import time
import requests


# list_proxy=[
#     'http://Username:Password@IP1:20000',
#     'http://Username:Password@IP2:20000',
#     'http://Username:Password@IP3:20000',
#     'http://Username:Password@IP4:20000',
#
# ]
# #
# proxy_cycle=cycle(list_proxy)
# proxy=next(proxy_cycle)

#
user_agents_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
]
#
# Header={'User-Agent': random.choice(user_agents_list),
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#         "Accept-Language":"en-Us,en;q=0.5",
#         "Connection":"keep-alive",
#         "Upgrade-Insecure-Requests":"1",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "none",
#         "Sec-Fetch-User": "?1",
#         "Cache-Control": "max-age=0",
#         }

def TakeUserInput():
    search_term=input('Job Title To Search:')
    search_term_url=search_term.replace(" ","+")
    location_term=input("Please input Location:")
    location_term_url=location_term.replace(" ","+")

    max_results=input(
        'Maximum Number of Pages to crawl at a time:'
    )

    try:
        max_results_int=int(max_results)
    except ValueError:
        print('Please enter a numnber and try again')
        exit(1)
    return [search_term_url,location_term_url,max_results_int]

job_details=[]
def getUrlPage():

    # URL = f"https://uk.indeed.com/?q={Position}&l={Location}&start={Page}"
    # try:
    #     for i in range(1,10):
    #         proxy=next(proxy_cycle)
    #         proxies={
    #             "http":proxy,
    #             "https":proxy
    #         }
    #         page = requests.get(URL, proxies=proxies)
    #         # return (page)
    # except Exception as e:
    #     print (e)
    url_variable=TakeUserInput()

    for start in range(0,url_variable[2],10):
        user_agent = random.choice(user_agents_list)
        headers = {'User-Agent': user_agent}
        source = 'https://www.indeed.co.uk/jobs?q=' + \
                 str(url_variable[0]) + '&l=' + \
                 str(url_variable[1]) + "&start=" + str(start)
        req=requests.get(source)
        print(req)
        exit()
        soup = BeautifulSoup(req.content(), 'html.parser')

        time.sleep(1)

        results=soup.find_all('div',attrs={'data-tn-component':'organicJob'})

        job_details.append(results)
        for x in results:
            date=x.find('span',attrs={'class':'date'})
            if date:
                date_str=date.text.strip()

    return job_details
def getUrlContent():
    soup = BeautifulSoup(getUrlPage().content, "html.parser")
    results = soup.find(id="ResultsContainer")
    return results

def getDivs():
    job_elements=getUrlContent().find_all("div",class_="card-content")

    for job_element in job_elements:
        title_element = job_element.find("h2", class_="title")
        company_element = job_element.find("h3", class_="company")
        location_element = job_element.find("p", class_="location")
        print(title_element.text.strip())
        print(company_element.text.strip())
        print(location_element.text.strip())
        print()

def getPythonJobs():
    python_jobs=getUrlContent().find_all("h2",string=lambda text:"python" in text.lower())

    for python_job in python_jobs:
        # title_element = python_job.find("h2", class_="title is-5")
        print(python_job.text.strip())
