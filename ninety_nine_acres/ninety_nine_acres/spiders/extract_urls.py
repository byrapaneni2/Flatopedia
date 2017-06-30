import scrapy
import pickle

def save_obj(obj, name):
    with open('obj/city_urls/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class NinetyNineAcres(scrapy.Spider):
    
    name = "extract_urls"

    def start_requests(self):
        cities = load_obj('cities')
        for city in cities:
            url = "http://www.99acres.com/new-projects-in-%s-ffid-page-1?property_type=1" % city
            yield scrapy.Request(url=url, callback=self.parse, meta={'city': city, 'page_num':1, 'urls':[]})

    def parse(self, response):
        page_num = response.meta['page_num']
        city = response.meta['city']
        urls = response.xpath("//div[@class='table_wrap']//td[@class='npsrp_head']/a/@href").extract()
        
        file = 'city_urls/%s.txt' % city
        with open(file, 'a') as f:
            for url in urls:
                f.write(url)
                f.write("\n")

        if page_num == 1:
            num_pages = response.xpath("//div[@class='pgdiv']//a[@class='pgsel']/@value").extract()[-1]
            for page_num in range(2,int(num_pages)+1):
                req_url = "http://www.99acres.com/new-projects-in-%s-ffid-page-%d?property_type=1" % (city, page_num)
                yield scrapy.Request(url=req_url, callback=self.parse, meta={'city':city,'page_num':page_num})
            
            
    

