#Upload Pubmed files as elastic search index

A. Download Pubmed XML files and keep in one folder
B. Run ./run_pubmed_preprocess.sh
This is dependent on pubmedxmltojson3.py
C. ./import_pubmed22.sh  
This is dependent on python preprocess22.py and uploads pubmed xml as .ndjson to elastic serach as bulk
