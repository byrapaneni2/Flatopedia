import scrapy
import json
import re
import os.path
from scrapy.http import HtmlResponse
import codecs

class NinetyNineAcres(scrapy.Spider):
    
    name = "extract_images"
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'scala (+http://www.scala.com)'
    }

    def start_requests(self):
        for i in range(1,2):
            path = "/Users/harish/Desktop/code/scrapy-projects/ninety_nine_acres/output/output%d.html" % i
            url = 'file://' + path
            if os.path.isfile(path):
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        project_id = response.xpath("//input[@id='npxidPROJ_ID']/@value").extract()[0] 
        urls = response.xpath("//div[@id='unitDetContainer']/div[@class='fpcRow flt flex qaOptionTuple dev_optionTuple']/div[@class='fpcColumn width17per flt alignC']/img/@data").extract()
        names = ["%s_%d" % (project_id,i) for i in range(len(urls))]
        yield {'image_urls': urls, 'image_names': names}
    