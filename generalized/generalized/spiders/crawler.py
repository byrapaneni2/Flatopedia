import scrapy
import pickle
import os
import re
import yaml
import json

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

# Load config file 
def load_yaml(name):
    with open(name +'.yaml') as f:
        config = yaml.load(f)
    return config


class Parser(scrapy.Spider):

    name = "parser"
    # start_urls = load_obj("urls")
    # start_urls = ["http://www.99acres.com/assetz-here-and-now-rachenahalli-bangalore-north-npxid-r271639?src=NPSRP"]
    # start_urls = ["http://www.99acres.com/assetz-63-degree-east-sarjapur-road-bangalore-east-npxid-r260370?src=NPSRP"]
    # start_urls = ["https://www.commonfloor.com/sreeda-pride-bangalore/povp-2yagtu"]
    start_urls = ["https://www.commonfloor.com/nitesh-napa-valley-bangalore/povp-on2p7o"]

    def parse(self, response):
        config = load_yaml("config1")

        project = {}
        for attr, value in config.iteritems():
            res = response.xpath(value["xpath"]).extract()
            if res:
                if len(res) == 1:
                    project[attr] = res[0]
                else:
                    project[attr] = res
            else:
                continue
            try:
                value["process"]
            except:
                continue
            try:
                for func in value["process"]:
                    exec("project[attr]" + " = " + func) 
            except:
                project.pop(attr, None)
                pass

        print json.dumps(project, indent=4, sort_keys=True)
        #save_obj(project, project["project_name"])


