import pickle
import os
import scrapy
import json
import re

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def price_to_decimal(price, price_unit):
    if price_unit == 'Lac' or price_unit == 'L':
        return price*10**5
    elif price_unit == 'Crore' or price_unit == 'Cr':
        return price*10**7


root = '/Users/harish/Desktop/code/scrapy-projects/commonfloor'
class CommonFloor(scrapy.Spider):

    name = "parser"

    def start_requests(self):
        cities = load_obj('cities')
        for city in cities:
            if not os.path.exists('html/'+city):
                continue

            if not os.path.exists('obj/parsed/'+city):
                os.makedirs('obj/parsed/'+city)

            for file in os.listdir('html/'+city):
                project_id = file
                url = 'file://%s/html/%s/%s' % (root,city,file)
                yield scrapy.Request(url=url, callback=self.parse, meta={'project_id':project_id, 'city':city})


    def parse(self, response):
        project = {}
        project_details = {}

        # project id
        project_details['project_id'] = response.meta['project_id']

        # project details
        details = response.xpath("//script[@type='application/ld+json']/text()").extract()
        if details:
            details = details[0]
            details = json.loads(details)

            name = details['name'].strip()
            project_details['name'] = name
            
            if 'address' in details.keys():
                if 'addressLocality' in details['address'].keys():
                    locality = details['address']['addressLocality']
                    project_details['locality'] = locality
                if 'addressRegion' in details['address'].keys():
                    city = details['address']['addressRegion']
                    project_details['city'] = city

            if 'geo' in details.keys():
                latitude = details['geo']['latitude']
                longitude = details['geo']['longitude']
                project_details['latitude'] = latitude
                project_details['longitude'] = longitude

        builder = response.xpath("//div[@id='about-project-builder']/div[1]/a/h2/text()").extract()
        if builder:
            project_details['builder'] = builder[0]

        builder_address = response.xpath("//div[@id='about-project-builder']/div[1]//p[@class='add']/text()").extract()
        if builder_address:
            project_details['builder_address'] = builder_address[0].strip()
        
        building_type = response.xpath("//div[@id='project-overview-details']//div[@class='row']/div[2]//span[@class='prolist']/text()").extract()
        if building_type:
            building_type = building_type[0]
            building_type = re.split('/', building_type)
            project_details['building_type'] = building_type

        status = response.xpath("//div[@id='project-overview-details']//div[@class='row']/div[1]//span[@class='prolist']/text()").extract()
        if status:
            project_details['status'] = status[0]

        dates = response.xpath("//div[@id='project-overview-details']//div[@class='row']/div[1]//div[@class='datatitle']/span/text()").extract()
        if dates:
            for date in dates:
                if re.search('Possession: ',date):
                    possession_date = re.sub('Possession: ', '', date)
                    possession_month, possession_year = re.split('-', possession_date)
                    possession_year = int(possession_year.strip())

                    project_details['possession_month'] = possession_month
                    project_details['possession_year'] = possession_year
                elif re.search('Launched: ',date):
                    launch_date = re.sub('Launched: ', '', date)
                    launch_month, launch_year = re.split('-', launch_date)
                    launch_year = int(launch_year.strip())

                    project_details['launch_month'] = launch_month
                    project_details['launch_year'] = launch_year
        
        # floor plans
        floor_plans = []
        fpans = response.xpath("//div[@id='house-details']/div[1]/div[@class='body']/div[@class='cf-tracking-enabled col']")
        for fpan in fpans:
            floor_plan = {}
            built_up_area = fpan.xpath("@data-sqft").extract()
            unit_bhk = fpan.xpath("@data-bhk").extract()
            unit_type = fpan.xpath("@data-type").extract()
            price = fpan.xpath("@data-price").extract()

            if built_up_area and built_up_area[0] != 'NA':
                built_up_area = built_up_area[0]
                built_up_area = re.findall('[0-9]+\.?[0-9]*', built_up_area)
                if built_up_area:
                    min_built_up_area = float(built_up_area[0])
                    max_built_up_area = float(built_up_area[-1])
                    floor_plan['min_built_up_area'] = min_built_up_area
                    floor_plan['max_built_up_area'] = max_built_up_area
                    floor_plan['min_built_up_area_units'] = 'sqft'
                    floor_plan['max_built_up_area_units'] = 'sqft'

            if unit_bhk:
                unit_bhk = unit_bhk[0]
                unit_bhk = re.sub('BHK', '', unit_bhk).strip()
                if unit_bhk:
                    unit_bhk = float(unit_bhk)
                    floor_plan['unit_bhk'] = unit_bhk

            if unit_type:
                floor_plan['unit_type'] = unit_type[0]

            if price and price[0] != 'NA':
                price = price[0]
                price_units = re.findall('L|Cr',price)
                price = re.findall('[0-9]+\.?[0-9]*',price)
                if price and price_units:
                    min_price = price_to_decimal(float(price[0]), price_units[0])
                    max_price = price_to_decimal(float(price[-1]), price_units[-1])
                    floor_plan['min_price'] = min_price
                    floor_plan['max_price'] = max_price

            floor_plans.append(floor_plan)

        # amenities
        amenities_list = response.xpath("//div[@id='amenities']//div[@class='amtlist clearfix']/ul/li/text()").extract()
        amenities_list = [amenity.strip() for amenity in amenities_list if amenity.strip()]
        amenities = {}
        for amenity in amenities_list:
            amenities[amenity] = True
        project['amenities'] = amenities

        project['project_details'] = project_details
        project['amenities'] = amenities
        project['floor_plans'] = floor_plans

        file = 'parsed/%s/%s' % (response.meta['city'],response.meta['project_id'])
        save_obj(project, file)
        """str_data = json.dumps(project)
        json_data = json.loads(str_data)
        with open('delete.txt', 'a') as f:
            f.write(json.dumps(json_data, indent=4, sort_keys=True))"""








