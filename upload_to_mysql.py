import peewee
from peewee import *
import pickle
import os
import json



def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

db = MySQLDatabase('sample', user='root',passwd='root')

class BaseModel(Model):
    class Meta:
        database = db

class Project(BaseModel):
    project_name = peewee.CharField(unique=True, null=False)
    builder = peewee.CharField(null=True)
    builder_address = peewee.CharField(null=True)
    completion_year = peewee.IntegerField(null=True)
    address = peewee.CharField(null=True)
    floors = peewee.IntegerField(null=True)
    max_area = peewee.FloatField(null=True)
    max_area_units = peewee.CharField(null=True)
    min_area = peewee.FloatField(null=True)
    min_area_units = peewee.CharField(null=True)
    max_price = peewee.FloatField(null=True)
    min_price = peewee.FloatField(null=True)
    total_area = peewee.FloatField(null=True)
    total_area_units = peewee.CharField(null=True)
    towers = peewee.IntegerField(null=True)
    bhks = peewee.CharField(null=True)
    units = peewee.IntegerField(null=True)
    building_type = peewee.CharField(null=True)
    locality = peewee.CharField(null=True)
    city = peewee.CharField(null=True)
    latitude = peewee.CharField(null=True)
    longitude = peewee.CharField(null=True)
    launch_year = peewee.IntegerField(null=True)
    launch_month = peewee.CharField(null=True)

class Amenity(BaseModel):
    amenity_name = peewee.CharField(unique=True, null=False)

class AmenityMapper(BaseModel):
    project_id = peewee.IntegerField()
    amenity_id = peewee.IntegerField()

class FloorPlan(BaseModel):
    project_id = peewee.IntegerField(null=False)
    bhk = peewee.FloatField(null=True)
    max_built_up_area = peewee.FloatField(null=True)
    min_built_up_area = peewee.FloatField(null=True)
    max_built_up_area_units = peewee.CharField(null=True)
    min_built_up_area_units = peewee.CharField(null=True)
    unit_type = peewee.CharField()
    min_unit_price = peewee.FloatField(null=True)
    max_unit_price = peewee.FloatField(null=True)
    bedroom = peewee.IntegerField(null=True)
    bathroom = peewee.IntegerField(null=True)
    balcony = peewee.IntegerField(null=True)
    carpet_area = peewee.FloatField(null=True)
    carpet_area_units = peewee.CharField(null=True)
    image = peewee.CharField(null=True)
    super_built_up_area = peewee.FloatField(null=True)
    super_built_up_area_units = peewee.CharField(null=True)
    poojaroom = peewee.IntegerField(null=True)
    storeroom = peewee.IntegerField(null=True)
    servantroom = peewee.IntegerField(null=True)
    

db.connect()
db.create_tables([Project, Amenity, AmenityMapper, FloorPlan], safe=True)

"""amenity_list = set(load_obj('obj/amenity_map.pkl').values())
for amenity in amenity_list:
    Amenity.insert(amenity_name=amenity).execute()"""

"""ctr = 0
projects = []
dirs = ['obj/combine', 'obj/nn', 'obj/cf']
for root  in dirs:
    for file in os.listdir(root):
        if os.path.isfile(file):
            continue

        if file.endswith(".pkl"):
            ctr += 1
            path = '%s/%s' % (root, file)
            project = load_obj(path)
            
            projects.append(project['project_details'])                

        if ctr%5000 == 0:
            print ctr
save_obj(projects, 'projects')"""

"""projects = load_obj('obj/projects.pkl')
with db.atomic():
    num = 1
    for idx in range(0, len(projects), num):
        if idx%1000 == 0:
            print idx
        try:
            Project.insert(projects[idx]).execute()
        except:
            pass"""

"""amenity_map = {}
amenity_list = set(load_obj('obj/amenity_map.pkl').values())
for amenity in amenity_list:
    amenity_map[amenity] = Amenity.get(amenity_name=amenity).id

amenity_mapper_list = []
dirs = ['obj/combine', 'obj/nn', 'obj/cf']
ctr = 0
for root  in dirs:
    for file in os.listdir(root):
        if os.path.isfile(file):
            continue

        if file.endswith(".pkl"):
            ctr += 1
            path = '%s/%s' % (root, file)
            project = load_obj(path)
            
            project_id = Project.get(project_name=project['project_details']['project_name']).id
            amenities = project['amenities']        
            for amenity in amenities:
                amenity_mapper_list.append({
                    'amenity_id': amenity_map[amenity],
                    'project_id': project_id
                    })   

        if ctr%1000 == 0:
            print ctr

with db.atomic():
    num = 100
    for idx in range(0, len(amenity_mapper_list), 100):
        if idx%1000 == 0:
            print idx
        AmenityMapper.insert_many(amenity_mapper_list[idx:idx+num]).execute()"""


"""dirs = ['obj/combine', 'obj/nn', 'obj/cf']
ctr = 0
floor_plan_list = []
for root  in dirs:
    for file in os.listdir(root):
        if os.path.isfile(file):
            continue

        if file.endswith(".pkl"):
            ctr += 1
            path = '%s/%s' % (root, file)
            project = load_obj(path)
            
            project_id = Project.get(project_name=project['project_details']['project_name']).id
            floor_plans = project['floor_plans']        
            for floor_plan in floor_plans:
                floor_plan['project_id'] = project_id
                floor_plan_list.append(floor_plan)   

        if ctr%1000 == 0:
            print ctr
save_obj(floor_plan_list, 'floor_plan_list')"""

floor_plan_list = load_obj('obj/floor_plan_list.pkl')
print len(floor_plan_list)
left = 0
with db.atomic():
    num = 1
    for idx in range(0, len(floor_plan_list), 100):
        if idx%1000 == 0:
            print idx
        try:
            FloorPlan.insert_many(floor_plan_list[idx:idx+num]).execute()
        except:
            left += 1

print left
db.close()



