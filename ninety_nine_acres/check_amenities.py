import pickle
import os
import re
import json

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

amenitycnt = {}
for idx, directory in enumerate(os.listdir('obj/parsed')):
	if os.path.isfile(directory):
		continue

	if idx == 3:
		break
	print directory
	for file in os.listdir('obj/parsed/'+directory):
		if not re.search('.pkl', file):
			continue
		file = 'parsed/%s/%s' % (directory, file)
		project = load_obj(file)
		amenities = project['amenities']

		details = project['project_details']
		try:
			month = details['completion_month']
		except KeyError:
			continue
		try:
			amenitycnt[month] += 1
		except KeyError:
			amenitycnt[month] = 1

		"""for key in amenities.keys():
			if key in amenitycnt.keys():
				amenitycnt[key] += 1
			else:
				amenitycnt[key] = 1"""

str_data = json.dumps(amenitycnt)
json_data = json.loads(str_data)
with open('delete.txt', 'w') as f:
    f.write(json.dumps(json_data, indent=4, sort_keys=True))