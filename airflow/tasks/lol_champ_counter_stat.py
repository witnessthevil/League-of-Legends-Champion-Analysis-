import scrapy 
import json
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import json
import re
from logger.Logger import Log
import psutil
import time
from pathlib import Path

logger = Log(__name__)

class CHAMPScraper(scrapy.Spider):

    name = "opggscrapying"
    allowed_domain = ['*']
    start_urls = ["https://www.metasrc.com/5v5/stats"]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
  
    def parse(self, response, **kwargs):  
        champ_list = response.xpath('//div[@id="table-scroll"]/table/tbody/tr')
        for champ in champ_list:
            name = champ.xpath('.//td/span/text()').get()
            link = champ.xpath('.//td/a/@href').get()
            yield response.follow(link, callback = self.scrape_champ, meta= {"champ_name":name})


    def scrape_champ(self, response, **kwargs):
            counter_list_with_win_rate = []
            countered_by_list_with_win_rate = []
            counter = response.xpath('//div[@class=" _sl4zvh _cn8bui tooltip-container"]/div[6]')
            countered_by = response.xpath('//div[@class=" _sl4zvh _cn8bui tooltip-container"]/div[7]')

            for i in counter.xpath('.//div/div/div/a'):
                champ_link = i.xpath('@href').get()[37:]
                champ = re.match(r'.+\/',champ_link).group()[:-1]
                win_rate = i.xpath('.//div/div[@class=" _9581uw"]/text()').get()
                win_rate_per = 51 + float(win_rate[1:])
                counter_list_with_win_rate.append([champ,win_rate_per])

            for i in countered_by.xpath('.//div/div/div/a'):
                champ_link = i.xpath('@href').get()[37:]
                champ = re.match(r'.+\/',champ_link).group()[:-1]
                win_rate = i.xpath('.//div/div[@class=" _9581uw"]/text()').get()
                win_rate_per = 49 - float(win_rate[1:])
                countered_by_list_with_win_rate.append([champ,win_rate_per])

            with open('/opt/airflow/zone1/lol_counter_stat.json','a') as f_in2:
                counter_list = {
                    "Champ_Name" : response.meta.get("champ_name"),
                    'champ_counter' : counter_list_with_win_rate,
                    'countered_by' : countered_by_list_with_win_rate
                }
    
                f_in2.write(json.dumps(counter_list) + '\n')




logger.logger.info("now scraping the champ counter stat")   
start_time  = time.perf_counter()
process = CrawlerProcess()
process.crawl(CHAMPScraper)
process.start() 
logger.logger.info("successfully scrape champ counter stat")   
end_time = time.perf_counter()
logger.logger.info(f"scrapying champ counter stat have used {end_time - start_time}s")
logger.logger.info(f"scrapying champ counter stat have used cpu {psutil.cpu_stats()}% and disk {psutil.disk_usage(Path(__file__))}%")