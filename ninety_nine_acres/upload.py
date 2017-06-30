import requests
import pickle
import os

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
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

def convertDictToAPIText(project):
    project_details = project['project_details']
    amenities = project['amenities']
    floor_plans = project['floor_plans']
    floor_plan_keys = project['floor_plan_keys']
    res = ''

    res += '==Project Details==\n'
    for key, value in project_details.iteritems():
        res += "* '''" + key + "''': [[" + key  + "::" + value + "]]\n"

    res += '==Amenities==\n'
    for key in amenities.keys():
        res += "* " + key + "\n"

    res += '==Floor Plans==\n'
    res += "{| class='wikitable'\n"
    res += "!"
    for key in floor_plan_keys:
        res += key + " || "
    res += "\n"

    for floor_plan in floor_plans:
        res += "|-\n"
        res += "|" 
        for key in floor_plan_keys:
            if key in floor_plan.keys():
                res += floor_plan[key] + " || "
            else:
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

    lgtoken, my_wiki_session = getLgToken(url, headers)
    my_wiki_BPsession = login(url, headers, my_wiki_session)
    csrftoken = getCSRFToken(url, headers, my_wiki_BPsession)

    ctr = 0
    for root, dirs, files in os.walk("obj"):
        for file in files:
            ctr += 1
            if file.endswith(".pkl"):
                project = load_obj(file)
                project_name = project['project_details']['project_name']
                APItext = convertDictToAPIText(project)
                num_characters = 0
                total_characters = len(APItext)
                print project_name
                while(num_characters < total_characters):
                    text = APItext[num_characters:min(num_characters+max_characters, total_characters)]
                    num_characters += max_characters
                    response = edit(url, headers, my_wiki_BPsession, title=project_name, appendtext=text)
                    print response

                if ctr >= 1:
                    break
        if ctr >= 1:
            break




#/mediawiki-1.28.2/api.php?action=edit&format=json&title=Jain&appendtext=Hello+world&token=a08de7e54fd6c88fe25470f6e4ea651a5938cf0a%2B%5C

























