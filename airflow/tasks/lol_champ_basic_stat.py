import scrapy 
import json
from scrapy.crawler import CrawlerProcess
import json
from logger.Logger import Log
import psutil
import time
import csv
from pathlib import Path

logger = Log(__name__)
class OPGGScraper(scrapy.Spider):

    name = "opggscrapying"
    allowed_domain = ['*']
    start_urls = ["https://www.metasrc.com/5v5/stats"]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        
    def parse(self, response, **kwargs):
        
        champ_list = response.xpath('//div[@id="table-scroll"]/table/tbody/tr')
        

        # ensure that everytime when it write stat to json file, it override the previous stat
        with open("/opt/airflow/zone1/lol_basic_stat.json","a") as f_in1: 
            #writer = csv.DictWriter(f_in1,fieldnames=["name","role","tier","score","trend","win_rate","role_per","pick_per","ban_per","kda"])
            #writer.writeheader()
            for champ in champ_list:
                name = champ.xpath('.//td/span/text()').get()
                role = champ.xpath('.//td[2]/div/text()').get()
                tier = champ.xpath('.//td[3]/text()').get()
                score = champ.xpath('.//td[4]/text()').get()
                trend = champ.xpath('.//td[5]/text()').get()
                win_rate = champ.xpath('.//td[6]/text()').get()
                role_per = champ.xpath('.//td[7]/text()').get()
                pick_per = champ.xpath('.//td[8]/text()').get()
                ban_per = champ.xpath('.//td[9]/text()').get()
                kda = champ.xpath('.//td[10]/text()').get()

                champ_stat = {
                    "champ" : name,
                    "role" : role,
                    "tier" : tier,
                    "score" : score,
                    "trend" : trend,  # if none, means it is new trend
                    "win_rate" : win_rate,
                    "role_per" : role_per,
                    "pick_per" : pick_per,
                    "ban_per" : ban_per,
                    "kda" : kda
                }

                f_in1.write(json.dumps(champ_stat) + '\n')

logger.logger.info("now scraping the champ basic stat")   
start_time  = time.perf_counter()
process = CrawlerProcess()
process.crawl(OPGGScraper)
process.start() 
logger.logger.info("successfully scrape champ basic stat")   
end_time = time.perf_counter()
logger.logger.info(f"scrapying champ stat have used {end_time - start_time}s")
logger.logger.info(f"scrapying champ stat have used cpu {psutil.cpu_stats()}% and disk {psutil.disk_usage(Path(__file__))}%")
