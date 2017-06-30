import scrapy
import pickle
import json
import re
import os

def save_obj(obj, name):
    with open('obj/'+name+'.pkl','w') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/'+name,'r') as f:
        return pickle.load(f)

attributes = {}
root = '/Users/harish/Desktop/code/scrapy-projects/cflisting'
class CFListing(scrapy.Spider):

    name = "parser"

    def start_requests(self):
        cities = ['bangalore', 'delhi', 'gurgaon', 'noida', 'ghaziabad', 'greater noida', 'faridabad', 'hyderabad', 'pune', 'mumbai']
        for city in cities:
            if not os.path.exists('html/'+city):
                continue

            if not os.path.exists('obj/parsed/'+city):
                os.makedirs('obj/parsed/'+city)

            for file in os.listdir('html/'+city):
                listing_id = file
                url = 'file://%s/html/%s/%s' % (root,city,file)
                yield scrapy.Request(url=url, callback=self.parse, meta={'listing_id':listing_id, 'city':city})

    def parse(self, response):
        city = response.meta['city']
        listing_id = response.meta['listing_id']
        listing_details = {}

        listing_details['project_name'] = response.xpath("//div[@class='master-plan-outer']//div[@class='e-model-wrapper']/p[@class='title']/text()").extract()
        
        keys = response.xpath("//div[@class='project-unit row card unit-detail-widget']//div[@class='about-unit-detail']//div[@class='row otherDetails']/div/p[1]/text()").extract()
        values = response.xpath("//div[@class='project-unit row card unit-detail-widget']//div[@class='about-unit-detail']//div[@class='row otherDetails']/div/p[2]/text()").extract()
        for key, value in zip(keys, values):
            if key in ['Listed by', 'Listed on']:
                continue
            listing_details[key] = value

        rooms = response.xpath("//div[@class='project-unit row card unit-detail-widget']//div[@class='about-unit-detail']/div[@class='row firstRow']/div/p/span[1]/text()").extract()
        num_rooms =  response.xpath("//div[@class='project-unit row card unit-detail-widget']//div[@class='about-unit-detail']/div[@class='row firstRow']/div/p/span[2]/text()").extract()
        for room, num_room in zip(rooms, num_rooms):
            if room == 'Bedrooms':
                listing_details['bedroom'] = num_room
            if room == 'Bathrooms':
                listing_details['bathroom'] = num_room

        overview = response.xpath("//div[@class='overview-page']/div[@class='project-detail row card']//div[@class='row']/div/div/p[@class='proj-title']/text()").extract()
        values = response.xpath("//div[@class='overview-page']/div[@class='project-detail row card']//div[@class='row']/div/div/p[@class='proj-value']")
        for key, value in zip(overview, values):
            if key == 'Carpet Area' or key == 'Possession':
                listing_details[key] = value.xpath("./text()").extract()[0]
            elif key == 'Price':
                listing_details[key] = value.xpath("./span[1]/text()").extract()[0]

        save_obj(listing_details, 'parsed/%s/%s'%(city, listing_id))


print attributes
with open('delete.txt','w') as f:
    f.write(json.dumps(attributes, indent=4, sort_keys=True))






