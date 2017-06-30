import pickle
import os

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

attr = set()
ctr = 0
for root, dirs, files in os.walk("obj"):
    for file in files:
        ctr += 1
        if file.endswith(".pkl"):
            if file == 'mediawiki_attributes.pkl':
                continue

            project = load_obj(file)
            project_details = project['project_details']
            amenities = project['amenities']
            
            for key, value in project_details.iteritems():
                attr.add(key)
            for key, value in amenities.iteritems():
                attr.add(key)
        if ctr%1000 == 0:
            print ctr

print len(attr)
save_obj(attr, 'mediawiki_attributes')
