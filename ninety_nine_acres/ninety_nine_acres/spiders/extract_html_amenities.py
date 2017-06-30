import scrapy
import os
import pickle


def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class NinetyNineAcres(scrapy.Spider):
    
    name = "extract_amenities"

    def start_requests(self):
        cities = load_obj('cities')
        for city in cities:
            if not os.path.exists('html/'+city):
                continue

            if not os.path.exists('amenities/'+city):
                    os.makedirs('amenities/'+city)

            for file in os.listdir('html/'+city):
                project_id = file
                url = "http://www.99acres.com/do/xid/xiddetail/createAmenitiesAjax/?resCom=R&projectId=%s&is_ajax=1" % project_id
                yield scrapy.Request(url=url, callback=self.parse, meta={'project_id':project_id, 'city':city})

    def parse(self, response):
        file = 'amenities/%s/%s' % (response.meta['city'], response.meta['project_id'])
        with open(file, 'w') as f:
            f.write(response.body)


























