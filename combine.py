import pickle
import json
import re
import json

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

def combinefunc(obj1,key1,obj2=None,key2=None,priority=0):
    if obj2 == None:
        try:
            return obj1[key1]
        except KeyError:
            return None

    if priority == 0:
        try:
            return obj1[key1]
        except KeyError:
            try:
                return obj2[key2]
            except KeyError:
                return None
    else:
        try:
            return obj2[key2]
        except KeyError:
            try:
                return obj1[key1]
            except KeyError:
                return None

cf = load_obj('commonfloor/obj/name_to_id.pkl')
nn = load_obj('ninety_nine_acres/obj/name_to_id.pkl')
amenity_map  =load_obj('obj/amenity_map.pkl')

match = 0
non_match = 0
count = 0
projects_parsed = {}
for proj_name in cf.keys():
    count += 1
    if count%1000 == 0:
        print count
    try:
        nn[proj_name]
        projects_parsed[proj_name] = True
        match += 1

        cfid = cf[proj_name]
        cfproj = load_obj('commonfloor/obj/parsed/%s.pkl'%cfid)
        nnid = nn[proj_name]
        nnproj = load_obj('ninety_nine_acres/obj/parsed/%s.pkl'%nnid)

        project = {}
        project_details = {}
        nnprojdet = nnproj['project_details']
        cfprojdet = cfproj['project_details']

        # Project details
        if combinefunc(nnprojdet,'project_name',cfprojdet,'name',0):
            project_details['project_name'] = combinefunc(nnprojdet,'project_name',cfprojdet,'name',0)
        if combinefunc(nnprojdet,'builder_name',cfprojdet,'builder',1):
            project_details['builder'] = combinefunc(nnprojdet,'builder_name',cfprojdet,'builder',1)
        if combinefunc(nnprojdet,'completion_year',cfprojdet,'possession_year',0):
            project_details['completion_year'] = combinefunc(nnprojdet,'completion_year',cfprojdet,'possession_year',0)
        if combinefunc(cfprojdet,'builder_address'):
            project_details['builder_address'] = combinefunc(cfprojdet,'builder_address')
        if combinefunc(nnprojdet,'address'):
            project_details['address'] = combinefunc(nnprojdet,'address')
        if combinefunc(nnprojdet,'floors'):
            project_details['floors'] = combinefunc(nnprojdet,'floors')
        if combinefunc(nnprojdet, 'max_area'):
            project_details['max_area'] = combinefunc(nnprojdet, 'max_area')
        if combinefunc(nnprojdet, 'max_area_units'):
            project_details['max_area_units'] = combinefunc(nnprojdet, 'max_area_units')
        if combinefunc(nnprojdet, 'min_area'):
            project_details['min_area'] = combinefunc(nnprojdet, 'min_area')
        if combinefunc(nnprojdet, 'min_area_units'):
            project_details['min_area_units'] = combinefunc(nnprojdet, 'min_area_units')
        if combinefunc(nnprojdet, 'max_price'):
            project_details['max_price'] = combinefunc(nnprojdet, 'max_price')
        if combinefunc(nnprojdet, 'min_price'):
            project_details['min_price'] = combinefunc(nnprojdet, 'min_price')
        if combinefunc(nnprojdet, 'total_area'):
            project_details['total_area'] = combinefunc(nnprojdet, 'total_area')
        if combinefunc(nnprojdet, 'total_area_units'):
            project_details['total_area_units'] = combinefunc(nnprojdet, 'total_area_units')
        if combinefunc(nnprojdet, 'towers'):
            project_details['towers'] = combinefunc(nnprojdet, 'towers')
        if combinefunc(nnprojdet, 'unit_bhk_types'):
            project_details['bhks'] = combinefunc(nnprojdet, 'unit_bhk_types')
        if combinefunc(nnprojdet, 'units'):
            project_details['units'] = combinefunc(nnprojdet, 'units')
        if combinefunc(cfprojdet, 'launch_month'):
            project_details['launch_month'] = combinefunc(cfprojdet, 'launch_month')
        if combinefunc(cfprojdet, 'launch_year'):
            project_details['launch_year'] = combinefunc(cfprojdet, 'launch_year')

        building_type = []
        try:
            building_type.extend(nnprojdet['building_type'])
            building_type.extend(cfprojdet['building_type'])
            project_details['building_type'] = list(set(building_type))
        except KeyError:
            try:
                building_type.extend(cfprojdet['building_type'])
                project_details['building_type'] = list(set(building_type))
            except KeyError:
                pass

        if combinefunc(nnprojdet,'locality',cfprojdet,'locality', 0):
            project_details['locality'] = combinefunc(nnprojdet,'locality',cfprojdet,'locality', 0)
        if combinefunc(nnprojdet,'city',cfprojdet,'city', 0):
            project_details['city'] = combinefunc(nnprojdet,'city',cfprojdet,'city', 0)
        if combinefunc(nnprojdet,'latitude',cfprojdet,'latitude',0):
            project_details['latitude'] = combinefunc(nnprojdet,'latitude',cfprojdet,'latitude',0)
        if combinefunc(nnprojdet,'longitude',cfprojdet,'longitude',0):
            project_details['longitude'] = combinefunc(nnprojdet,'longitude',cfprojdet,'longitude',0)


        # floor plans
        floor_plans = []
        for i, floor_plan in enumerate(nnproj['floor_plans']):
            try:
                nnproj['floor_plans'][i]['min_unit_price'] = nnproj['floor_plans'][i].pop('min_new_booking_base_price')
            except KeyError:
                pass
            try:
                nnproj['floor_plans'][i]['max_unit_price'] = nnproj['floor_plans'][i].pop('max_new_booking_base_price')
            except KeyError:
                pass
            try:
                nnproj['floor_plans'][i]['image'] = nnproj['floor_plans'][i].pop('img_src')
            except KeyError:
                pass
            try:
                nnproj['floor_plans'][i]['bhk'] = nnproj['floor_plans'][i].pop('unit_bhk')
            except KeyError:
                pass
        
        for i, floor_plan in enumerate(cfproj['floor_plans']):
            try:
                cfproj['floor_plans'][i]['bhk'] = cfproj['floor_plans'][i].pop('unit_bhk')
            except KeyError:
                pass
            try:
                cfproj['floor_plans'][i]['min_unit_price'] = cfproj['floor_plans'][i].pop('min_price')
            except KeyError:
                pass
            try:
                cfproj['floor_plans'][i]['max_unit_price'] = cfproj['floor_plans'][i].pop('max_price')
            except KeyError:
                pass

        try:
            floor_plans.extend(nnproj['floor_plans'])
            floor_plans.extend(cfproj['floor_plans'])
        except KeyError:
            try:
                floor_plans.extend(cfproj['floor_plans'])
            except KeyError:
                pass

        amenities = []
        nnamenities = nnproj['amenities']
        nnamenities = [amenity_map[amenity] for amenity in nnamenities.keys()]
        amenities.extend(nnamenities)
        cfamenities = cfproj['amenities']
        cfamenities = [amenity_map[amenity] for amenity in cfamenities.keys()]
        amenities.extend(cfamenities)
        amenities = list(set(amenities))

        project['project_details'] = project_details
        project['floor_plans'] = floor_plans
        project['amenities'] = amenities
        id1 = re.split('/',nn[proj_name])[1]
        id2 = re.split('/',cf[proj_name])[1]
        save_obj(project,'combine/%s_%s'%(id1,id2))
        
        """str_data = json.dumps(project)
        json_data = json.loads(str_data)
        with open('delete.txt', 'a') as f:
            f.write(json.dumps(json_data, indent=4, sort_keys=True))"""
        
                
    except KeyError:
        projects_parsed[proj_name] = True
        non_match += 1

        cfid = cf[proj_name]
        cfproj = load_obj('commonfloor/obj/parsed/%s.pkl'%cfid)

        project = {}
        project_details = {}
        cfprojdet = cfproj['project_details']

        # Project details
        if combinefunc(cfprojdet,'name'):
            project_details['project_name'] = combinefunc(cfprojdet,'name')
        if combinefunc(cfprojdet,'builder'):
            project_details['builder'] = combinefunc(cfprojdet,'builder')
        if combinefunc(cfprojdet,'possession_year'):
            project_details['completion_year'] = combinefunc(cfprojdet,'possession_year')
        if combinefunc(cfprojdet,'builder_address'):
            project_details['builder_address'] = combinefunc(cfprojdet,'builder_address')
        if combinefunc(cfprojdet, 'launch_month'):
            project_details['launch_month'] = combinefunc(cfprojdet, 'launch_month')
        if combinefunc(cfprojdet, 'launch_year'):
            project_details['launch_year'] = combinefunc(cfprojdet, 'launch_year')

        building_type = []
        try:
            building_type = cfprojdet['building_type']
            project_details['building_type'] = building_type
        except KeyError:
            pass

        if combinefunc(cfprojdet,'locality'):
            project_details['locality'] = combinefunc(cfprojdet,'locality')
        if combinefunc(cfprojdet,'city'):
            project_details['city'] = combinefunc(cfprojdet,'city')
        if combinefunc(cfprojdet,'latitude'):
            project_details['latitude'] = combinefunc(cfprojdet,'latitude')
        if combinefunc(cfprojdet,'longitude'):
            project_details['longitude'] = combinefunc(cfprojdet,'longitudes')


        # floor plans
        floor_plans = []
        for i, floor_plan in enumerate(cfproj['floor_plans']):
            try:
                cfproj['floor_plans'][i]['bhk'] = cfproj['floor_plans'][i].pop('unit_bhk')
            except KeyError:
                pass
            try:
                cfproj['floor_plans'][i]['min_unit_price'] = cfproj['floor_plans'][i].pop('min_price')
            except KeyError:
                pass
            try:
                cfproj['floor_plans'][i]['max_unit_price'] = cfproj['floor_plans'][i].pop('max_price')
            except KeyError:
                pass
        floor_plans = cfproj['floor_plans']

        # amenities
        cfamenities = cfproj['amenities']
        cfamenities = [amenity_map[amenity] for amenity in cfamenities.keys()]
        amenities = list(set(cfamenities))

        project['project_details'] = project_details
        project['floor_plans'] = floor_plans
        project['amenities'] = amenities

        id = re.split('/',cf[proj_name])[1]
        save_obj(project,'cf/%s'%id)

        """str_data = json.dumps(project)
        json_data = json.loads(str_data)
        with open('delete.txt', 'a') as f:
            f.write(json.dumps(json_data, indent=4, sort_keys=True))"""

print match, non_match, len(cf.keys())
print count

match = 0
non_match = 0
count = 0

for proj_name in nn.keys():
    count += 1
    if count%1000 == 0:
        print count 
    try:
        cf[proj_name]
        match += 1
    except KeyError:
        non_match += 1
        projects_parsed[proj_name] = True

        nnid = nn[proj_name]
        nnproj = load_obj('ninety_nine_acres/obj/parsed/%s.pkl'%nnid)

        project = {}
        project_details = {}
        nnprojdet = nnproj['project_details']

        # Project details
        if combinefunc(nnprojdet,'project_name'):
            project_details['project_name'] = combinefunc(nnprojdet,'project_name')
        if combinefunc(nnprojdet,'builder_name'):
            project_details['builder'] = combinefunc(nnprojdet,'builder_name')
        if combinefunc(nnprojdet,'completion_year'):
            project_details['completion_year'] = combinefunc(nnprojdet,'completion_year')
        if combinefunc(nnprojdet,'address'):
            project_details['address'] = combinefunc(nnprojdet,'address')
        if combinefunc(nnprojdet,'floors'):
            project_details['floors'] = combinefunc(nnprojdet,'floors')
        if combinefunc(nnprojdet, 'max_area'):
            project_details['max_area'] = combinefunc(nnprojdet, 'max_area')
        if combinefunc(nnprojdet, 'max_area_units'):
            project_details['max_area_units'] = combinefunc(nnprojdet, 'max_area_units')
        if combinefunc(nnprojdet, 'min_area'):
            project_details['min_area'] = combinefunc(nnprojdet, 'min_area')
        if combinefunc(nnprojdet, 'min_area_units'):
            project_details['min_area_units'] = combinefunc(nnprojdet, 'min_area_units')
        if combinefunc(nnprojdet, 'max_price'):
            project_details['max_price'] = combinefunc(nnprojdet, 'max_price')
        if combinefunc(nnprojdet, 'min_price'):
            project_details['min_price'] = combinefunc(nnprojdet, 'min_price')
        if combinefunc(nnprojdet, 'total_area'):
            project_details['total_area'] = combinefunc(nnprojdet, 'total_area')
        if combinefunc(nnprojdet, 'total_area_units'):
            project_details['total_area_units'] = combinefunc(nnprojdet, 'total_area_units')
        if combinefunc(nnprojdet, 'towers'):
            project_details['towers'] = combinefunc(nnprojdet, 'towers')
        if combinefunc(nnprojdet, 'unit_bhk_types'):
            project_details['bhks'] = combinefunc(nnprojdet, 'unit_bhk_types')
        if combinefunc(nnprojdet, 'units'):
            project_details['units'] = combinefunc(nnprojdet, 'units')

        try:
            building_type = nnprojdet['building_type']
            project_details['building_type'] = building_type
        except KeyError:
            pass

        if combinefunc(nnprojdet,'locality'):
            project_details['locality'] = combinefunc(nnprojdet,'locality')
        if combinefunc(nnprojdet,'city'):
            project_details['city'] = combinefunc(nnprojdet,'city')
        if combinefunc(nnprojdet,'latitude'):
            project_details['latitude'] = combinefunc(nnprojdet,'latitude')
        if combinefunc(nnprojdet,'longitude'):
            project_details['longitude'] = combinefunc(nnprojdet,'longitude')


        # floor plans
        floor_plans = []
        for i, floor_plan in enumerate(nnproj['floor_plans']):
            try:
                nnproj['floor_plans'][i]['min_unit_price'] = nnproj['floor_plans'][i].pop('min_new_booking_base_price')
            except KeyError:
                pass
            try:
                nnproj['floor_plans'][i]['max_unit_price'] = nnproj['floor_plans'][i].pop('max_new_booking_base_price')
            except KeyError:
                pass
            try:
                nnproj['floor_plans'][i]['image'] = nnproj['floor_plans'][i].pop('img_src')
            except KeyError:
                pass
            try:
                nnproj['floor_plans'][i]['bhk'] = nnproj['floor_plans'][i].pop('unit_bhk')
            except KeyError:
                pass        
        floor_plans = nnproj['floor_plans']

        #amenities
        nnamenities = nnproj['amenities']
        nnamenities = [amenity_map[amenity] for amenity in nnamenities.keys()]
        amenities = list(set(nnamenities))

        project['project_details'] = project_details
        project['floor_plans'] = floor_plans
        project['amenities'] = amenities
        id = re.split('/',nn[proj_name])[1]
        save_obj(project,'nn/%s'%id)

        """str_data = json.dumps(project)
        json_data = json.loads(str_data)
        with open('delete.txt', 'a') as f:
            f.write(json.dumps(json_data, indent=4, sort_keys=True))"""


print match, non_match, len(nn.keys())
print count
print len(projects_parsed.keys())