import pickle

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('obj/city_urls/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

cities = load_obj('cities')
cnt = 0
for city in cities:
	urls = []
	with open('city_urls/'+city+'.txt','r') as f:
		for i, url in enumerate(f):
			urls.append(url)
		print city, len(urls)
		cnt += len(urls)
		save_obj(urls, city)

print cnt

