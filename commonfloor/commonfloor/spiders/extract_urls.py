import scrapy 
import pickle

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class CommonFloor(scrapy.Spider):
	name = "extract_urls"
	page_size = 300

	def start_requests(self):
		start_url = "https://www.commonfloor.com/"
		end_url = "-property/projects?page=1&page_size=%d" % self.page_size
		cities = load_obj('cities')
		cities = ['bangalore','chennai','greater noida','gurgaon','hyderabad','jalna','kolkata','noida','pune']
		for city in cities:
			url = start_url+city+end_url
			yield scrapy.Request(url=url, callback=self.parse, meta={'city':city, 'urls': [], 'page_num': 1})
	

	def parse(self, response):
		base_url = "https://www.commonfloor.com"
		urls = response.xpath("//div[@class='card cards-list']//div[@class='row projectTitle']//div[@class='projectName clearfix']//a/@href").extract()
		urls = [base_url+url for url in urls]
		city = response.meta['city']
		if len(urls) == self.page_size:
			page_num = response.meta['page_num']+1
			end_url = "-property/projects?page=%d&page_size=%d" % (page_num, self.page_size)
			req_url = base_url + "/" + city + end_url
			urls.extend(response.meta['urls'])
			yield scrapy.Request(url=req_url, callback=self.parse, meta={'city':city, 'urls': urls, 'page_num': page_num})
		else:
			urls.extend(response.meta['urls'])
			save_obj(urls, 'urls_' + city)

