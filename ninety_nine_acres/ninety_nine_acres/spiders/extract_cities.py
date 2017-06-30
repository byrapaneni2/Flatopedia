import scrapy
import pickle
import re

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class NinetyNineAcres(scrapy.Spider):

	name = 'extract_cities'
	start_urls = ["http://www.99acres.com/Home-Real-Estate.htm"]

	def parse(self, response):
		cities = response.xpath("//div[@class='footerWraper']//ul[@class='ftcity']/li/a/text()").extract()
		cities = [re.sub(' / ','-',city.lower()) for city in cities]
		save_obj(cities, 'cities')