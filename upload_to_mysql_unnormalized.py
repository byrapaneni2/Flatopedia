import peewee
from peewee import *
import pickle
import os
import json
import copy



def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

db = MySQLDatabase('sample', user='root',passwd='root')

class BaseModel(Model):
    class Meta:
        database = db

class ProjectUnnormalized(BaseModel):
    project_name = peewee.CharField(null=False)
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

    Street_Light = BooleanField(default=False)
    Waste_Management_System = BooleanField(default=False)
    Foosball = BooleanField(default=False)
    Rock_Climbing = BooleanField(default=False)
    Video_Intercom = BooleanField(default=False)
    Outdoor_games = BooleanField(default=False)
    Squash_Court = BooleanField(default=False)
    Gazebo = BooleanField(default=False)
    Ayurvedic_Centre = BooleanField(default=False)
    Gated_Community = BooleanField(default=False)
    Volley_Ball_Court = BooleanField(default=False)
    Party_Lawn = BooleanField(default=False)
    Car_Wash_Area = BooleanField(default=False)
    Bar_Chill_Out_Lounge = BooleanField(default=False)
    Petrol_Pump = BooleanField(default=False)
    Smart_Card_Entry = BooleanField(default=False)
    Solar_Lighting = BooleanField(default=False)
    Golf_Course = BooleanField(default=False)
    Dart_Board = BooleanField(default=False)
    Kids_Pool = BooleanField(default=False)
    Restaurant = BooleanField(default=False)
    Sand_Pit = BooleanField(default=False)
    Rain_Water_Harvesting = BooleanField(default=False)
    Wifi = BooleanField(default=False)
    Multipurpose_Court = BooleanField(default=False)
    Landscaped_Garden = BooleanField(default=False)
    Beach_Volley_Ball_Court = BooleanField(default=False)
    Bowling = BooleanField(default=False)
    Business_Lounge = BooleanField(default=False)
    Anti_termite_treatment = BooleanField(default=False)
    Borewell = BooleanField(default=False)
    Laundromat = BooleanField(default=False)
    Amphitheatre = BooleanField(default=False)
    Changing_Area = BooleanField(default=False)
    Reading_Lounge = BooleanField(default=False)
    Concierge_Service = BooleanField(default=False)
    Clinic = BooleanField(default=False)
    Fire_Fighting_System = BooleanField(default=False)
    Spa = BooleanField(default=False)
    Overhead_tank = BooleanField(default=False)
    Terrace_Party_Area = BooleanField(default=False)
    School = BooleanField(default=False)
    Pharmacy = BooleanField(default=False)
    Covered_Parking = BooleanField(default=False)
    Audio_Visual_Hall = BooleanField(default=False)
    Guest_House = BooleanField(default=False)
    Fire_Extinguisher = BooleanField(default=False)
    Toilet_for_drivers = BooleanField(default=False)
    High_Speed_Elevator = BooleanField(default=False)
    Card_Room = BooleanField(default=False)
    Food_Court = BooleanField(default=False)
    Locker_Room_Facilities = BooleanField(default=False)
    Go_Karting = BooleanField(default=False)
    Lift = BooleanField(default=False)
    Yoga_Aerobics_Meditation_Area = BooleanField(default=False)
    DTH_Television = BooleanField(default=False)
    Valet_Parking = BooleanField(default=False)
    Theatre = BooleanField(default=False)
    Gaming_Cafe = BooleanField(default=False)
    Maintenance_Staff = BooleanField(default=False)
    Indoor_Games = BooleanField(default=False)
    Club_House = BooleanField(default=False)
    Skating_Rink = BooleanField(default=False)
    Cricket_Pitch = BooleanField(default=False)
    Paved_Compound = BooleanField(default=False)
    Home_Automation = BooleanField(default=False)
    Security = BooleanField(default=False)
    Cigar_Lounge = BooleanField(default=False)
    Fire_Alarm = BooleanField(default=False)
    Name_Plates = BooleanField(default=False)
    Power_Backup_Lift = BooleanField(default=False)
    Visitors_Parking = BooleanField(default=False)
    Vaastu = BooleanField(default=False)
    Pool_Table = BooleanField(default=False)
    Jacuzzi_Steam_Sauna = BooleanField(default=False)
    Conference_room = BooleanField(default=False)
    Service_Lift = BooleanField(default=False)
    Waiting_Lounge = BooleanField(default=False)
    Hr_Water_Supply = BooleanField(default=False)
    Football_Ground = BooleanField(default=False)
    Acupressure_Walkway = BooleanField(default=False)
    Multipurpose_Hall = BooleanField(default=False)
    Natural_Pond = BooleanField(default=False)
    ATM = BooleanField(default=False)
    Car_Wash = BooleanField(default=False)
    Community_Hall = BooleanField(default=False)
    Open_Parking = BooleanField(default=False)
    Fountain = BooleanField(default=False)
    Tennis_Court = BooleanField(default=False)
    Temple = BooleanField(default=False)
    Basketball_Court = BooleanField(default=False)
    Air_Hockey = BooleanField(default=False)
    Jogging_Track = BooleanField(default=False)
    Lawn = BooleanField(default=False)
    Solar_Water_Heating = BooleanField(default=False)
    Super_Market = BooleanField(default=False)
    Shopping_Centre = BooleanField(default=False)
    Water_Treatment_Plant = BooleanField(default=False)
    Senior_Citizen_Park = BooleanField(default=False)
    Flower_Garden = BooleanField(default=False)
    Piped_Gas = BooleanField(default=False)
    Swimming_Pool = BooleanField(default=False)
    Security_Cabin = BooleanField(default=False)
    Broadband_Internet = BooleanField(default=False)
    Aerobics_Centre = BooleanField(default=False)
    Gymnasium = BooleanField(default=False)
    Library = BooleanField(default=False)
    CCTV_Camera = BooleanField(default=False)
    Organic_Waste_Converter = BooleanField(default=False)
    Drainage_and_Sewage_Treatment = BooleanField(default=False)
    Car_Parking = BooleanField(default=False)
    Barbecue = BooleanField(default=False)
    Creche = BooleanField(default=False)
    Terrace_Garden = BooleanField(default=False)
    Pergola = BooleanField(default=False)
    Medical_Centre = BooleanField(default=False)
    Billiards = BooleanField(default=False)
    Plantation = BooleanField(default=False)
    Banquet_Hall = BooleanField(default=False)
    Chess = BooleanField(default=False)
    Reflexology_Park = BooleanField(default=False)
    Table_Tennis = BooleanField(default=False)
    Pneumatic_Water_Lines = BooleanField(default=False)
    Laundry = BooleanField(default=False)
    Home_Theater = BooleanField(default=False)
    Intercom = BooleanField(default=False)
    RO_System = BooleanField(default=False)
    Cycling_Track = BooleanField(default=False)
    Sun_Deck = BooleanField(default=False)
    Pucca_Road = BooleanField(default=False)
    Bank = BooleanField(default=False)
    Power_Backup = BooleanField(default=False)
    Recreation = BooleanField(default=False)
    Manicured_Garden = BooleanField(default=False)
    Doctor_on_Call = BooleanField(default=False)
    Letter_Box = BooleanField(default=False)
    Milk_Booth = BooleanField(default=False)
    Escalators = BooleanField(default=False)
    Sewage = BooleanField(default=False)
    Infinity_Pool = BooleanField(default=False)
    Salon = BooleanField(default=False)
    Earthquake_Resistant = BooleanField(default=False)
    Badminton_Court = BooleanField(default=False)
    Play_Area = BooleanField(default=False)
    Carrom = BooleanField(default=False)
    Party_Area = BooleanField(default=False)
    Entrance_Lobby = BooleanField(default=False)
    AC_Lobby = BooleanField(default=False)
    Bus_Shelter = BooleanField(default=False)
    Cafeteria = BooleanField(default=False)
    Departmental_Store = BooleanField(default=False)

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
db.create_tables([ProjectUnnormalized], safe=True)

ctr = 0
projects = []
dirs = ['obj/combine', 'obj/nn', 'obj/cf']
"""for root  in dirs:
    for file in os.listdir(root):
        if os.path.isfile(file):
            continue

        if file.endswith(".pkl"):
            path = '%s/%s' % (root, file)
            project = load_obj(path)

            project_values = project['project_details']

            amenities = {}
            for amenity in project['amenities']:
                amenities[amenity] = True            
            project_values.update(amenities)

            floor_plans = project['floor_plans']        
            for floor_plan in floor_plans:
                ctr += 1
                project_record = project_values.copy()
                project_record.update(floor_plan)

                projects.append(project_record)             

                if ctr%5000 == 0:
                    print ctr
            if len(floor_plans) == 0:
                projects.append(project_values) """


#save_obj(projects, 'projects')
#print projects
projects = load_obj('obj/projects.pkl')
print len(projects)
left = 0
with db.atomic():
    num = 1
    for idx in range(0, len(projects), num):
        if idx%1000 == 0:
            print idx, left
        try:
            ProjectUnnormalized.insert(projects[idx]).execute()
        except:
            left += 1
            pass

"""amenity_map = {}
amenity_list = set(load_obj('obj/amenity_map.pkl').values())
for amenity in amenity_list:
    amenity_map[amenity] = Amenity.get(amenity_name=amenity).id"""

"""amenity_mapper_list = []
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

"""floor_plan_list = load_obj('obj/floor_plan_list.pkl')
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
            left += 1"""

db.close()



