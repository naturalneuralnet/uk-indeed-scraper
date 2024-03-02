import scrapy
import re
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup

class IndeedspiderSpider(scrapy.Spider):
    name = "indeedspider"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

    def get_indeed_search_url(self, keyword, location, offset=0):
        # filter set to to one to remove duplicates
        parameters = {"q": keyword, "l": location, "filter": 0, "start": offset}
        return "https://uk.indeed.com/jobs?" + urlencode(parameters)


    def start_requests(self):
        print("PRINTING LOCATION")
        # print(self.location)
        # print(self.keywords)
        keyword_list = ['junior devops']
        #keyword_list = [self.keywords]
        location_list = ["London"]
        for keyword in keyword_list:
            for location in location_list:
                indeed_jobs_url = self.get_indeed_search_url(keyword, location)
                yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results, meta={'keyword': keyword, 'location': location, 'offset': 0})

    # takes the response back from the requests
    # uses regex
    # checks if there are multiple pages of jobs
    def parse_search_results(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword'] 
        offset = response.meta['offset'] 
        script_tag  = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])

            ## Extract Jobs From Search Page
            jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
            
            for index, job in enumerate(jobs_list):
                if job.get('jobkey') is not None:
                    job_url = 'https://uk.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=' + job.get('jobkey')
                    yield scrapy.Request(url=job_url, 
                            callback=self.parse_job, 
                            meta={
                                'keyword': keyword, 
                                'location': location, 
                                'page': round(offset / 10) + 1 if offset > 0 else 1,
                                'position': index,
                                'jobKey': job.get('jobkey'),
                                'jobURL': job_url
                            })

            
            # Paginate Through Jobs Pages
            if offset == 0:
                meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
                num_results = sum(category["jobCount"] for category in meta_data)
                number_of_jobs = 10
                # int(response.css('div.jobsearch-JobCountAndSortPane-jobCount span::text').get().split(' ')[0])
                
               
                if number_of_jobs > 80:
                    number_of_jobs = 50
              
                for offset in range(10, number_of_jobs, 10):
                    url = self.get_indeed_search_url(keyword, location, offset)
                    
                    yield scrapy.Request(url=url, callback=self.parse_search_results, meta={'keyword': keyword, 'location': location, 'offset': offset})   

    # Gets the jobs data for each job
    def parse_job(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword'] 
        page = response.meta['page'] 
        position = response.meta['position'] 
        script_tag  = re.findall(r"_initialData=(\{.+?\});", response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]
            job_reqs = ''
            if job['jobDescriptionSectionModel'] is not None:
                job_reqs = job['jobDescriptionSectionModel']['qualificationsSectionModel']
            else:
                job_reqs = 'NONE'
            yield {
                'keyword': keyword,
                'location': location,
                'page': page,
                'position': position,
                'company': job.get('jobInfoHeaderModel').get('companyName'),
                'jobkey': response.meta['jobKey'],
                'jobTitle': job.get('jobInfoHeaderModel').get('jobTitle'),
                'jobURL': response.meta['jobURL'],
                'jobRequirements': job_reqs,
                'maxSalary': job.get('estimatedSalary').get('max') if job.get('estimatedSalary') is not None else 0,
                'minSalary': job.get('estimatedSalary').get('min') if job.get('estimatedSalary') is not None else 0,
                'jobDescription': ' '.join(BeautifulSoup(job['sanitizedJobDescription'], "html.parser").stripped_strings)
            }
