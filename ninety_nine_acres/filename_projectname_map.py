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

name_to_id = {}
id_to_name = {}
for directory in os.listdir('obj/parsed'):
	if os.path.isfile(directory):
		continue

	print directory
	for filename in os.listdir('obj/parsed/'+directory):
		if not re.search('.pkl', filename):
			continue
		
		file = 'parsed/%s/%s' % (directory, filename)
		project = load_obj(file)
		
		project_name = project['project_details']['project_name']
		project_id = '%s/%s' % (directory, re.sub('.pkl','',filename))

		name_to_id[project_name] = project_id
		id_to_name[project_id] = project_name

save_obj(name_to_id, 'name_to_id')
save_obj(id_to_name, 'id_to_name')

mapper = load_obj('id_to_name.pkl')
str_data = json.dumps(mapper)
json_data = json.loads(str_data)
with open('delete.txt', 'w') as f:
    f.write(json.dumps(json_data, indent=4, sort_keys=True))