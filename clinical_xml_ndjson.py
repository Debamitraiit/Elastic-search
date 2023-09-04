import os
import xml.etree.ElementTree as ET
import json

path = "."


def find_thing(root, field_name):
    if root.find(f".//*[@Name='{field_name}']") is not None:
        return root.find(f".//*[@Name='{field_name}']").text
    else:
        return root.find(f".//*[@Name='{field_name}']")


def find_many_things(root, field_name):
    return ','.join([item.text for item in root.findall(f".//*[@Name='{field_name}']")])
    

output_dict = {}



for filename in os.listdir(path):
    if not filename.endswith("xml"):
        continue
    tree = ET.parse(filename)
    root = tree.getroot()

    rank = root.attrib['Rank']

    nctid = find_thing(root, 'NCTId')
    
    
    brief_summary = find_thing(root, 'BriefSummary')

    brief_title = find_thing(root, 'BriefTitle')
    
    detailed_summary = find_thing(root, 'DetailedDescription')
    
    
    condition_mesh_term = find_many_things(root, 'ConditionMeshTerm')


    output_dict["NCTID"] = nctid
    output_dict["rank"] = rank

    output_dict["Title"] = brief_title
    
    output_dict["briefsummary"] = brief_summary
    output_dict["mesh"] = condition_mesh_term
    output_dict["details"] = detailed_summary

    print(f"Processing file:{filename}")
    
    
    with open(f"output_{rank}.json", "w+") as f:
        f.write(f"{json.dumps(output_dict)}\n")

#Uploading as elastic search repository
import requests, json, os
from elasticsearch import Elasticsearch

directory = '/home/ubuntu/clinical/cxml'

res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

i = 1

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        fullpath=os.path.join(directory, filename)
        f = open(fullpath)
        docket_content = f.read()
        # Send the data into es
        es.index(index='clinical2', ignore=400, doc_type='docket', 
        id=i, body=json.loads(docket_content))
        i = i + 1
