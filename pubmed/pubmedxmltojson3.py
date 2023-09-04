import html
import json
import sys
import gzip
import re
from lxml import etree

def clean_text(text):
    """ removes HTML tags and superscripts """
    # remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # remove superscripts
    text = re.sub(r'<sup>.*?</sup>', '', text)
    text = re.sub(r'<sub>.*?</sub>', '', text)

    # Remove brackets
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove parentheses
    text = re.sub(r'\(.*?\)', '', text)
    
    # Add a space after removing subscripts and superscripts
    text = re.sub(r'</sub>|</sup>', r'\g<0> ', text)
    return text.strip()

def format_(text, na_value=''):
    """ formats text """
    if not text:
        return na_value
    text = clean_text(text)
    if not text:
        return na_value
    return html.unescape(text)

def get_pmid(doc):
    """ returns pmid and pmid version """
    pmid = doc.find('PMID').text.strip()
    pmid_version = doc.find('PMID').attrib.get('Version', '').strip()
    return pmid, pmid_version

def get_title_abstract_citation(doc):
    """ returns title, abstract and citation """
    title = format_(doc.find('./Article/ArticleTitle').text)

    citation = format_(doc.find('./Article/Journal/Title').text)

    abstract = []
    for abstract_part in doc.findall('./Article/Abstract/AbstractText'):
        label = abstract_part.get('Label', '').strip()
        abstract_part = label + ': ' + format_(abstract_part.text) if label else format_(abstract_part.text)
        abstract.append(abstract_part)

    return title, abstract, citation

def get_meshterms(doc):
    """ return mesh terms """
    mesh_terms = set()
    for mesh_headings in doc.findall('./MeshHeadingList'):
        for mesh_heading in mesh_headings.findall('./MeshHeading'):
            for desc in mesh_heading.findall('./DescriptorName'):
                mesh_term = desc.text.strip()
                mesh_term = format_(mesh_term)
                if mesh_term:
                    mesh_terms.add(mesh_term)

    return list(mesh_terms)

def get_keywords(doc):
    """ returns keywords """
    keywords = set()
    for keyword_list in doc.findall('./KeywordList'):
        for keyword in keyword_list.findall('./Keyword'):
            if keyword.text is not None:
                keyword = format_(keyword.text)
                if keyword:
                    keywords.add(keyword)
    return list(keywords)

def main(filename):
    with gzip.open(filename) as infile:
        data = infile.read()
    # remove XML declaration
    if data.startswith(b'<?xml'):
        data = data.split(b'\n', 1)[1]
    # parse XML with lxml.etree
    parser = etree.XMLParser(strip_cdata=False)
    root = etree.fromstring(data, parser=parser)
    # remove HTML tags and superscripts
    etree.strip_tags(root, 'b', 'i', 'u', 'a', 'img', 'sup', 'sub')
    for citation in root.findall('./PubmedArticle/MedlineCitation'):
        pmid, pmid_version = get_pmid(citation)
        try:
            meshterm = get_meshterms(citation)
            keyword = get_keywords(citation)
            title, abstract, citation = get_title_abstract_citation(citation)
            rec = dict(pmid=pmid, pmidVersion=pmid_version, citation=citation, title=title, abstract=abstract,
                       mesh_terms=meshterm, keywords=keyword)
            print(json.dumps(rec))
        except:
            pass

if __name__ == '__main__':
    main(sys.argv[1])
