<h1> XML to JSON to Elastic Search Index</h1

<h2>Prerequisite</h2>

<h6>1. Elastic Search and Kibana installed</h6>
<h6>2. Pubmed xml, Clinical Trial xml and patent xml files downloaded</h6>

<h1>What do the codes do?</h1>

<h5>1. Converting Clinical Trial XML data to .ndjson to upload as an elastic search index (clinical_xml_ndjson.py)</h5>
<h5>2. Converting Pubmed XML to .ndjson</h5>
<h5>3. Converting patent XML to .ndjson and uploading as elastic search index (patent_to_ES.py): This code uses BeautifulSoup </h5>


<h3>Upload Clinical Trials files as elastic search index</h3>

<p>Download Clinical Trials XML files: https://classic.clinicaltrials.gov/ct2/resources/download</p>

<p>Use the code clinical_xml_ndjson.py</p>


<h3>Upload Pubmed files as elastic search index</h3>



<h5>Download the pubmed xml dump</h5>

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


<h3>Upload Patent files as elastic search index</h3>
Download Patent XML files: https://developer.uspto.gov/product/patent-application-full-text-dataxml

Use the code patent_to_ES.py

## Contributors ✨

Thanks go to these wonderful people

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href=""><img src="" width="100px;" alt="SC"/><br /><sub><b>Subhodeep Chatterjee</b></sub></a><br /></a></td>
       <td align="center" valign="top" width="14.28%"><a href=""><img src="" width="100px;" alt="VS"/><br /><sub><b>Vikas Sharma</b></sub></a><br /></a></td>
    </tr>
    
  </tbody>
</table>
