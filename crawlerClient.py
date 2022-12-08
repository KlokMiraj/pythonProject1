from scrapfly import ScrapflyClient,ScrapeConfig
import asyncio
import re
from typing import list
from urllib.parse import urlencode

def TakeUserInput():
    search_job=input('Please Input the position:')
    search_job_temp=search_job.replace(" ","+")
    search_location=input('PLease Input the location')
    search_location_temp=search_location.reaplace(" ","+")
    max_page_per_input=input('Pages you wanna get per search')

    try:
        max_page_int = int(max_page_per_input)
    except ValueError:
        print('Please Enter a valid integer')

    return [search_job_temp,search_location_temp,max_page_int]

def parse_serach_page(result):
    data=re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});',result.content)
    data=json.loads(data[0])
    return {
        "results": data["metaData"]["mosaicProviderJobCardsModel"]["results"],
        "meta":data["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
    }

async def GetScrapUlrClient(client: ScrapflyClient, query:str,location:str,source_url):
    def make_page_url(offset):
        parameters={"q":query, "l":location, "filter":0,"start":offset}
        return source_url+urlencode(parameters)

    # client=ScrapflyClient(key=api_key)
    # result=client.scrape(ScrapeConfig(url=source_url,asp=True))
    #
    # return result.content

    print(f"scraping first page of search: {query=}, {location=}")
    result_first_page=await client.async_scrape(
        Scrapeconfig(
            make_page_url(0),
            country="US",
            asp=True
        )
    )
    data_first_page=parse_serach_page(result_first_page)
    results=data_first_page["results"]
    total_results=sum(category['jobCount'] for category in data_first_page["meta"])
    if total_results>1000:
        total_results=1000

    print(f"scraping remaining {total_results-10/10}pages")
    other_pages=[
        ScrapeConfiguration(url=make_page_url(offset),country="US", asp=True) for offset in range(10,total_result+10,10)
    ]
    async for result in client.concurrent_scrape(other_pages):
        try:
            data=parse_serach_page(result)
            results.extend(data["results"])
        except Exception as e:
            print(e)
    return results

def parse_job_parse(result: ScrapeApiResponse):
    """""parse job data from job listing page"""
    data=re.findall(r"_intitalData=({.+?});",result.content)
    data=json.loads(data[0])
    return data["jobInfoWrapperModel"]["jobInfoModel"]

async def scrape_jobs(client:ScrapflyClient, job_key:List[str]):
    """""scrape job page"""
    urls=[f"https://www.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk={job_key}"]
    scraped=[]
    async for result in clien.concurrent_scrape([ScrapeConfig(url=urls),country="US",asp=True) for url in urls]):
            scraped.append(parse_job_page(result))
    return scraped

async def main(api_key:str):
    with ScrapflyClient(Key=api_key,max_concurrency=2) as client:
        serach_results=await scrape_serach(client,"python","Texas")
        print(json.dunps(search_results,indent=2))
        _found_job_ids=[result["jobkey"] for result in serach_results]
        job_results=await scrape_jobs(client,job_keys=_foundjob_ids[:10])
        print(json.dump(job_results,indent=2))

