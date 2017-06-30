#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 12:12:11 2017

@author: harish
"""

import scrapy
import json
import re
import os
import pickle

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def price_to_decimal(price, price_unit):
    if price_unit == 'Lac':
        return price*10**5
    elif price_unit == 'Crore':
        return price*10**7

root = '/Users/harish/Desktop/code/scrapy-projects/ninety_nine_acres'

class NinetyNineAcres(scrapy.Spider):
    
    name = "parser"
    projects = {}

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

    """start_urls = []
    for i in range(0,5):
        path = "/Users/harish/Desktop/code/scrapy-projects/ninety_nine_acres/output/output%d.html" % i
        url = "file:///Users/harish/Desktop/code/scrapy-projects/ninety_nine_acres/output/output%d.html" % i
        if os.path.isfile(path):
            start_urls.append(url)
        #start_urls.append("file:///Users/harish/Desktop/code/scrapy-projects/ninety_nine_acres/test.html")"""
        
        
    def parse(self, response):

        project_details = {}
        project = {}

        project_id = response.meta['project_id']
        project_details['project_id'] = project_id
        """project_id = response.xpath("//input[@id='npxidPROJ_ID']/@value").extract()
        if project_id:
            project_id = project_id[0]
            project_details['project_id'] = project_id
        else:
            lgfile = open('log.txt', 'a')
            lgfile.write('No project_id in file ')
            lgfile.write(response.url)
            lgfile.write('\n\n')
            lgfile.close()
            yield"""

        # project details
        builder_name = response.xpath("//input[@id='npxidBUILDER_NAME']/@value").extract()
        project_name = response.xpath("//input[@id='npxidPROJ_NAME']/@value").extract()
        address = response.xpath("//input[@id='npxidPROJ_ADD']/@value").extract()
        locality = response.xpath("//input[@id='npxidPROJ_LOCALITY']/@value").extract()
        city = response.xpath("//input[@id='npxidPROJ_CITY']/@value").extract()
        min_price = response.xpath("//input[@id='npxidMIN_PRICE']/@value").extract()
        max_price = response.xpath("//input[@id='npxidMAX_PRICE']/@value").extract()
        min_area = response.xpath("//input[@id='npxidMIN_AREA_SQFT']/@value").extract()
        max_area = response.xpath("//input[@id='npxidMAX_AREA_SQFT']/@value").extract()
        latitude = response.xpath("//input[@id='npxidLATITUDE']/@value").extract()
        longitude = response.xpath("//input[@id='npxidLONGITUDE']/@value").extract()

        if builder_name:
            project_details['builder_name'] = builder_name[0]
        if project_name:
           project_details['project_name'] = project_name[0]
        if min_price:
           min_price = float(min_price[0])
           project_details['min_price'] = min_price
        if max_price:
           max_price = float(max_price[0])
           project_details['max_price'] = max_price
        if min_area:
           min_area = float(min_area[0])
           project_details['min_area'] = min_area
           project_details['min_area_units'] = 'sqft'
        if max_area:
           max_area = float(max_area[0])
           project_details['max_area'] = max_area
           project_details['max_area_units'] = 'sqft'
        if latitude:
           project_details['latitude'] = latitude[0]
        if longitude:
           project_details['longitude'] = longitude[0]
        if locality:
           project_details['locality'] = locality[0]
        if city:
           project_details['city'] = city[0]
        if address:
           project_details['address'] = address[0]
        
        #overview
        overview = response.xpath("//div[@id='overviewSection']")
        facts = overview.xpath(".//div[@class='factBox']")
        factLbls = []
        for idx, factobj in enumerate(facts):
            factLbl = factobj.xpath(".//div[contains(@class,'factLbl')]/text()").extract()
            if len(factLbl) == 1:
                factLbl = factLbl[0]
            else:
                factLbl = factLbl[-2]
            factLbl = factLbl.strip()

            #[u'Possession', u'Address', u'Project Details', u'Configurations', u'New Booking Base Price', u'Resale Price', u'Total Project Area', u'Saleable Area']
            if factLbl == 'Possession':
                status = factobj.xpath(".//div[@class='factVal1']/text()").extract()
                completion_date = factobj.xpath(".//div[@class='factVal2']/text()").extract()
                
                if status:
                  project_details['status'] = status[0]
                if completion_date:
                  completion_date = completion_date[0]
                  completion_date = re.sub('Completed in', '', completion_date).strip()

                  completion_year = re.findall("[0-9]+", completion_date)
                  if completion_year:
                    completion_year = int(completion_year[0])
                    project_details['completion_year'] = completion_year 
                  completion_month = re.findall("[a-zA-Z]+", completion_date)
                  if completion_month:
                    project_details['completion_month'] = completion_month[0]

                  project_details['completion_date'] = completion_date

            elif factLbl == 'Project Details':
                val1 = factobj.xpath(".//div[@class='factVal1']/text()").extract()
                val2 = factobj.xpath(".//div[@class='factVal2']/text()").extract()
                
                if val1:
                    val1 = val1[0]
                    val1 = val1.strip()
                    
                    # if val1 is not empty
                    if val1:
                        val1 = re.split('; ', val1)
                        for val in val1:
                            if re.findall('Units', val):
                                units = re.split(' ', val)[0]
                                units = int(units)
                                project_details['units'] = units
                            if re.findall('Towers', val):
                                towers = re.split(' ', val)[0]
                                towers = int(towers)
                                project_details['towers'] = towers
                if val2:
                    val2 = val2[0]
                    if re.findall('Floors', val2):
                        floors = re.split(' ', val2)[0]
                        floors = int(floors)
                        project_details['floors'] = floors

            elif factLbl == 'Configurations':
                building_type = factobj.xpath(".//div[@class='factVal1']/text()").extract()
                unit_bhk_types = factobj.xpath(".//div[@class='factVal2']/text()").extract()
                
                if building_type:
                    building_type = building_type[0]
                    building_type = building_type.split(',')
                    building_type = [x.strip() for x in building_type]
                    project_details['building_type'] = building_type
                if unit_bhk_types:
                    unit_bhk_types = unit_bhk_types[0]
                    unit_bhk_types = re.findall('[0-9]+',unit_bhk_types)
                    unit_bhk_types = [int(unit_bhk_type.strip()) for unit_bhk_type in unit_bhk_types]
                    project_details['unit_bhk_types'] = unit_bhk_types

            elif factLbl == 'Total Project Area':
                area = factobj.xpath(".//div[@class='factVal1']/text()").extract()
                if area:
                    area = area[0]
                    total_area = re.findall('\d+\.*\d*', area)[0]
                    total_area = float(total_area)
                    total_area_units = re.findall('[a-zA-Z]+', area)[0]
                    
                    project_details['total_area'] = total_area
                    project_details['tota_area_units'] = total_area_units


            factLbls.append(factLbl)
        project['project_details'] = project_details

        floor_plans = []
        floor_plan_keys = ['unit_bhk', 'img_src', 'bedroom', 'bathroom', 'balcony', 'super_built_up_area', 'carpet_area', 'min_new_booking_base_price', 'max_new_booking_base_price', 'pooja_room', 'store_room', 'servant_room']
        fpans = response.xpath("//div[@class='floorPlanContainer']//div[@id='unitDetContainer']/div[@class='fpcRow flt flex qaOptionTuple dev_optionTuple']")
        for fpan in fpans:
            floor_plan = {}

            unit_bhk = fpan.xpath("./@data-property-type").extract()
            if unit_bhk:
                unit_bhk = unit_bhk[0]
                unit_bhk = re.split(' ', unit_bhk)[0]
                if unit_bhk == "Residential" or unit_bhk == 'Commercial':
                    continue
                unit_bhk = int(unit_bhk)
                floor_plan['unit_bhk'] = unit_bhk
            
            img_src = fpan.xpath("./div[contains(@class,'alignC')]/img/@data").extract()
            if img_src:
                floor_plan['img_src'] = img_src[0]

            inclusions = fpan.xpath("./div[contains(@class,'qaInclusions')]/text()").extract()
            for inclusion in inclusions:
                inclusion = inclusion.strip()
                if inclusion:
                    if re.findall('Bedroom', inclusion):
                        bedroom = re.split(' ', inclusion)[0]
                        bedroom = int(bedroom)
                        floor_plan['bedroom'] = bedroom
                    elif re.findall('Bathroom', inclusion):
                        bathroom = re.split(' ', inclusion)[0]
                        bathroom = int(bathroom)
                        floor_plan['bathroom'] = bathroom
                    elif re.findall('Balcony', inclusion):
                        balcony = re.split(' ', inclusion)[0]
                        balcony = int(balcony)
                        floor_plan['balcony'] = balcony
                    elif re.findall('Pooja Room', inclusion):
                        poojaroom = re.findall('[0-9]+', inclusion)
                        if poojaroom:
                            poojaroom = int(poojaroom[0])
                            floor_plan['poojaroom'] = poojaroom
                        else:
                            floor_plan['poojaroom'] = 1
                    elif re.findall('Servant Room', inclusion):
                        servantroom = re.findall('[0-9]+', inclusion)
                        if servantroom:
                            servantroom = int(servantroom[0])
                            floor_plan['servantroom'] = servantroom
                        else:
                            floor_plan['servantroom'] = 1
                    elif re.findall('Store Room', inclusion):
                        storeroom = re.findall('[0-9]+', inclusion)
                        if storeroom:
                            storeroom = int(storeroom[0])
                            floor_plan['storeroom'] = storeroom
                        else:
                            floor_plan['storeroom'] = 1

            
            area = fpan.xpath("./div[contains(@class,'qaAreaDiv')]/div")
            for ar in area:
                attr = ar.xpath("./span[1]/text()").extract()
                if attr:
                    attr = attr[0]
                    attr = attr.strip()

                    if re.findall('Super Built-up Area', attr):
                        super_built_up_area = ar.xpath("./span[@class='jumboText']/text()").extract()
                        super_built_up_area_units = ar.xpath("./span[@class='jumboText']/em/text()").extract()
                        if super_built_up_area:
                            super_built_up_area = super_built_up_area[0]
                            super_built_up_area = super_built_up_area.strip()
                            super_built_up_area = float(super_built_up_area)
                            floor_plan['super_built_up_area'] = super_built_up_area
                        if super_built_up_area_units:
                            super_built_up_area_units = super_built_up_area_units[0].lower()
                            floor_plan['super_built_up_area_units'] = super_built_up_area_units

                    if re.findall('Carpet Area', attr):
                        carpet_area = ar.xpath("./span[@class='jumboText']/text()").extract()
                        carpet_area_units = ar.xpath("./span[@class='jumboText']/em/text()").extract()
                        if carpet_area:
                            carpet_area = carpet_area[0]
                            carpet_area = carpet_area.strip()
                            carpet_area = float(carpet_area)
                            floor_plan['carpet_area'] = carpet_area
                        if carpet_area_units:
                            carpet_area_units = carpet_area_units[0].lower()
                            floor_plan['carpet_area_units'] = carpet_area_units

            new_booking_base_price = fpan.xpath("./div[contains(@class,'qaNewBookingPriceDiv')]//span/text()").extract()
            if new_booking_base_price:
                new_booking_base_price = new_booking_base_price[0]
                new_booking_base_price =  new_booking_base_price.strip()
                if new_booking_base_price == 'Not Available' or new_booking_base_price == 'Price on Request':
                    pass
                elif re.search('-', new_booking_base_price):
                    new_booking_base_price = re.split(' ', new_booking_base_price)
                    min_new_booking_base_price = new_booking_base_price[1]
                    if new_booking_base_price[2] == 'Lac' or new_booking_base_price[2] == 'Crore':
                        min_price_unit = new_booking_base_price[2]
                        min_new_booking_base_price = price_to_decimal(float(min_new_booking_base_price), min_price_unit)
                        max_new_booking_base_price = new_booking_base_price[4]
                        max_price_unit = new_booking_base_price[5]
                        max_new_booking_base_price = price_to_decimal(float(max_new_booking_base_price), max_price_unit)
                    else:
                        price_unit = new_booking_base_price[4]        
                        min_new_booking_base_price = price_to_decimal(float(min_new_booking_base_price), price_unit)
                        max_new_booking_base_price = new_booking_base_price[3]
                        max_new_booking_base_price = price_to_decimal(float(max_new_booking_base_price), price_unit)

                    floor_plan['min_new_booking_base_price'] = min_new_booking_base_price
                    floor_plan['max_new_booking_base_price'] = max_new_booking_base_price
                else:
                    new_booking_base_price = re.split(' ', new_booking_base_price)
                    price_unit = new_booking_base_price[2]
                    min_new_booking_base_price = max_new_booking_base_price = price_to_decimal(float(new_booking_base_price[1]), price_unit)
                    floor_plan['min_new_booking_base_price'] = min_new_booking_base_price
                    floor_plan['max_new_booking_base_price'] = max_new_booking_base_price

            # resale price is not a factual information
            """resale_price = fpan.xpath("./div[contains(@class,'qaResalePriceDiv')]/div/span[@class='jumboText']/text()").extract()
            if resale_price:
                resale_price = resale_price[0]
                resale_price = resale_price.strip()
                floor_plan['resale_price'] = resale_price"""

            floor_plans.append(floor_plan)
        project['floor_plans'] = floor_plans
        project['floor_plan_keys'] = floor_plan_keys


        path = "%s/amenities/%s/%s" % (root,response.meta['city'],project_id)
        url = "file://%s/amenities/%s/%s" % (root,response.meta['city'],project_id)
        if os.path.isfile(path):
            yield scrapy.Request(url=url, 
                                callback = self.parse_amenities,
                                meta={'project_id': project_id, 'city': response.meta['city'], 'project':project})
        else:
            print "file not there"

    def parse_amenities(self, response):
        amenities = {}
        basic_amn = response.xpath("//div[@class='xidBasicAmn floatl ']/div[2]/div")
        for amn_obj in basic_amn:
            #amn_val = amn_obj.xpath("./div/text()").extract()[0]
            amn_key = amn_obj.xpath("./i/@class").extract()
            if amn_key:
                amn_key = amn_key[0]
                amn_key = re.split(' ', amn_key)[-1]
                amn_key = re.split('xid_', amn_key)[-1]
                amn_key = re.sub('_light','',amn_key)
                amenities[amn_key] = True

        other_amn = response.xpath("//div[@class='xidPrmListCont']/ul/li[not(contains(@class,'amnSubHead')) and not(contains(@class,'liSpacer')) and not(contains(@class,'amnSubHead twoLiners'))]/text()").extract()
        for amn in other_amn:
            amenities[amn] = True

        project = response.meta['project']
        project_id = response.meta['project_id']

        project['amenities'] = amenities
        self.projects[project_id] = project

        file = 'parsed/%s/%s' % (response.meta['city'],project_id)
        save_obj(project, file)

        """str_data = json.dumps(project)
        json_data = json.loads(str_data)
        with open('delete.txt', 'a') as f:
            f.write(json.dumps(json_data, indent=4, sort_keys=True))"""


















            
























