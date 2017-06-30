import scrapy 
import pickle

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class CommonFloor(scrapy.Spider):

	name = "extract_cities"
	start_urls = ["https://www.commonfloor.com/sitemap"]

	def parse(self, response):
		cities = response.xpath("//div[@class='city-name col-xs-2']/a/text()").extract()
		cities = [city.strip().lower() for city in cities]
		save_obj(cities, 'cities')
		print cities