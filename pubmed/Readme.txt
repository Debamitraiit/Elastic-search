# <b>Upload Pubmed files as elastic search index </b>



#Download the pubmed xml dump

wget -r --no-parent --no-remove-listing ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/*.xml.gz

wget -r --no-parent --no-remove-listing ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/*.xml.gz

mkdir pubmed
mv pubmed*.xml.gz pubmed/.

#pre-process the Pubmed xml to json
run_pubmed_preprocess.sh

mkdir pubmed/json

mv pubmed/pubmed22n*.json.bz2 pubmed/json/.

#upload json to ES database (entire pubmed)
import_pubmed22.sh
