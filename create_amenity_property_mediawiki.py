import requests
import pickle
import os
import ast

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
def edit(url, headers, csrftoken, my_wiki_BPsession, title, text="", appendtext=""):
    if text == "":
        querystring = {"action":"edit","title":title,'format': 'json', "appendtext": appendtext}
    else:
        querystring = {"action":"edit","title":title,'format': 'json', "text":text}
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % (csrftoken)
    cookies = {'my_wiki_BPsession': my_wiki_BPsession}

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, cookies=cookies)
    return response

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    url = "http://localhost:8888/mediawiki-1.28.2/api.php"
    headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache"
    }

    lgtoken, my_wiki_session = getLgToken(url, headers)
    my_wiki_BPsession = login(url, headers, my_wiki_session)
    csrftoken = getCSRFToken(url, headers, my_wiki_BPsession)

    amenity_map = load_obj('amenity_map.pkl')
    for amenity in amenity_map.values():
        amenity = amenity.title()
        title = "Property:%s" % amenity
        text = "This property is of type [[Has type:: Boolean]]"
        response = edit(url, headers, csrftoken, my_wiki_BPsession, title=title, text=text)
        print response.text

        response_text = ast.literal_eval(response.text)
        try:
       		if response_text["error"]["code"] == 'badtoken':
       			csrftoken = getCSRFToken(url, headers, my_wiki_BPsession)
            	response = edit(url, headers, csrftoken, my_wiki_BPsession, title=title, text=text)
            	print response.text
       	except KeyError:
       		pass






























