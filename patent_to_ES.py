import xml.etree.ElementTree as ET
import json
import os
import html
from bs4 import BeautifulSoup

path = "."

output_dict = {}


for filename in os.listdir(path):
    if not filename.endswith("XML"):
        continue
    
    tree = ET.parse(filename)
    root = tree.getroot()

    file = root.attrib['file'].split("-")[0]

    
    
    
    xml_text = html.unescape(open(filename, 'r').read())

# Split out patent applications / grants
    for patent in xml_text.split("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"):
  
  # Skip if it doesn't exist
        if patent is None or patent == "":
            continue 
  
  # Load patent text as HTML document
        bs = BeautifulSoup(patent)  
        #print(bs)

  # Search patent for application 
        application = bs.find('us-patent-application')
  
  # If no application, search for grant

        publication_title = bs.find('invention-title').text
        #file = bs.find['file'].text
        
        publication_date = bs.find('publication-reference').find('date').text
        application_type = bs.find('application-reference')['appl-type']
        
        #print(application_type)
    
        output_dict["file"] = file
        output_dict["title"] = publication_title
        output_dict["date"] = publication_date
        output_dict["type"] = application_type
        
        
        for el in bs.find_all('abstract'):
            output_dict["abstract"] = el.text
            
       
            
        for el in bs.find_all('description'):
            output_dict["description"] = el.text
            
        
        
        
        #print(output_dict)
        print(f"Processing file:{filename}")
    
    
        with open(f"output_{file}.json", "w+") as f:
            f.write(f"{json.dumps(output_dict)}\n")

## Uploading as ELastic search index
import requests, json, os
from elasticsearch import Elasticsearch

directory = '/home/ubuntu/patents/pxml'

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
        es.index(index='patent', ignore=400, doc_type='docket', 
        id=i, body=json.loads(docket_content))
        i = i + 1