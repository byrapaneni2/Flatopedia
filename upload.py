import requests
import pickle
import os
import ast
import re

# get login token
def getLgToken(url, headers):
    querystring = {"action":"query",
                    "meta":"tokens",
                    "type":"login",
                    "format":"json"}
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data;"

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    my_wiki_session = response.cookies['my_wiki_session']
    lgtoken = response.json()['query']['tokens']['logintoken']
    return lgtoken, my_wiki_session

#login
def login(url, headers, my_wiki_session):
    querystring = {"action":"login",
                    "lgname":"Harishrithish7@nestaway",
                    'format':"json"}
    lgpassword = 'b30b2r8lgtjla1a2h7k5ephm6vaqq6kl'
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"lgpassword\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"lgtoken\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % (lgpassword, lgtoken)
    cookie = {'my_wiki_session': my_wiki_session}

    response = requests.request("POST", url, data=payload, headers=headers, 
                                    params=querystring, cookies=cookie)
    my_wiki_BPsession = response.cookies['my_wiki_BPsession']
    return my_wiki_BPsession

# get csrf token
def getCSRFToken(url, headers, my_wiki_BPsession):
    querystring = {"action":"query","meta":"tokens",'format':'json'}
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; "
    cookie = {'my_wiki_BPsession': my_wiki_BPsession}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring, cookies=cookie)
    csrftoken = response.json()['query']['tokens']['csrftoken']
    return csrftoken

# create or edit the page
def edit(url, headers, my_wiki_BPsession, title, text="", appendtext=""):
    if text == "":
        querystring = {"action":"edit","title":title,'format': 'json', "appendtext": appendtext}
    else:
        querystring = {"action":"edit","title":title,'format': 'json', "text":text}
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % (csrftoken)
    cookie = {'my_wiki_BPsession': my_wiki_BPsession}

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, cookies=cookie)
    return response

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

def convertDictToAPIText(project, floor_plan_keys):
    project_details = project['project_details']
    amenities = project['amenities']
    floor_plans = project['floor_plans']
    res = ''

    res += '==Project Details==\n'
    for key, value in project_details.iteritems():
        key = re.sub('_',' ',key)
        key = key.title()
        if isinstance(value, unicode):
            res += "* '''" + key + "''': [[" + key  + "::" + value.encode('utf-8') + "]]\n"
        elif isinstance(value, list):
            res += "* '''" + key + "''': "
            for idx, item in enumerate(value):
                if isinstance(item, unicode):
                    res += "[[" + key  + "::" + item.encode('utf-8') + "]]"
                else:
                    res += "[[" + key  + "::" + str(item) + "]]"
                if idx != len(value)-1:
                    res += ", "
            res += "\n"
        else:
            res += "* '''" + key + "''': [[" + key  + "::" + str(value) + "]]\n"

    res += '==Amenities==\n'
    for key in amenities:
        res += "* [[" + key + ":: True| " + key + "]]\n"

    keys_length = len(floor_plan_keys)
    res += '==Floor Plans==\n'
    res += "{| class='wikitable'\n"
    res += "!"
    for idx, key in enumerate(floor_plan_keys):
        key = re.sub('_',' ',key)
        key = key.title()
        res += key
        if idx != keys_length-1:
            res += " || "
    res += "\n"

    for floor_plan in floor_plans:
        res += "|-\n"
        res += "|" 
        for idx, key in enumerate(floor_plan_keys):
            if key in floor_plan.keys():
                value = floor_plan[key]
                key = re.sub('_',' ',key)
                key = key.title()
                if isinstance(value, unicode):
                    res += "[[" + key + "::" + value.encode('utf-8') + "]]"
                else:
                    res += "[[" + key + "::" + str(value) + "]]"
                if idx != keys_length-1:
                    res += " || "
            elif idx != keys_length-1:
                res += " || "
        res += "\n"
    res += "|}\n"

    return res

if __name__ == '__main__':
    url = "http://localhost:8888/mediawiki-1.28.2/api.php"
    headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache"
    }
    max_characters = 5000
    floor_plan_keys = ['bhk', 'image', 'bedroom', 'bathroom', 'balcony', 'super_built_up_area', 'carpet_area', 'min_price', 'max_price', 'pooja_room', 'store_room', 'servant_room', 'max_built_up_area', 'min_built_up_area']

    lgtoken, my_wiki_session = getLgToken(url, headers)
    my_wiki_BPsession = login(url, headers, my_wiki_session)
    csrftoken = getCSRFToken(url, headers, my_wiki_BPsession)

    ctr = 0
    for root, dirs, files in os.walk("obj/combine"):
        for file in files:
            if file.endswith(".pkl") and file != 'amenity_map.pkl':
                ctr += 1
                path = '%s/%s' % (root, file)
                project = load_obj(path)
                project_name = project['project_details']['project_name']
                print project_name
                APItext = convertDictToAPIText(project, floor_plan_keys)
                
                num_characters = 0
                total_characters = len(APItext)
                while num_characters < total_characters:
                    text = APItext[num_characters:min(num_characters+max_characters, total_characters)]
                    if num_characters == 0:
                        response = edit(url, headers, my_wiki_BPsession, title=project_name, text=text)
                    else:
                        response = edit(url, headers, my_wiki_BPsession, title=project_name, appendtext=text)
                    print response.text

                    response_text = ast.literal_eval(response.text)
                    try:
                        if response_text["error"]["code"] == 'badtoken':
                            csrftoken = getCSRFToken(url, headers, my_wiki_BPsession)
                            if num_characters == 0:
                                response = edit(url, headers, my_wiki_BPsession, title=project_name, text=text)
                            else:
                                response = edit(url, headers, my_wiki_BPsession, title=project_name, appendtext=text)
                            print response.text
                    except KeyError:
                        pass
                    num_characters += max_characters

                if ctr >= 100:
                    break
        if ctr >= 100:
            break




#/mediawiki-1.28.2/api.php?action=edit&format=json&title=Jain&appendtext=Hello+world&token=a08de7e54fd6c88fe25470f6e4ea651a5938cf0a%2B%5C

























