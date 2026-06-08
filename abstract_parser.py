import xml.etree.ElementTree as ET
import json

def parse_abstract(xml_text):
    """Parse XML abstract and return clean dictionary."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None
    
    article = root.find(".//PubmedArticle")
    if article is None:
        return None
    
    title = article.findtext(".//ArticleTitle", default="No Title")
    
    abstract_parts = article.findall(".//AbstractText")
    abstract = " ".join([a.text for a in abstract_parts if a.text])
    
    authors = []
    for author in article.findall(".//Author"):
        last = author.findtext("LastName", default="")
        first = author.findtext("ForeName", default="")
        if last:
            authors.append(f"{last} {first}".strip())
            
    year = article.findtext(".//PubDate/Year", default="Unknown")
    journal = article.findtext(".//Journal/Title", default="Unknown")
    pmid = article.findtext(".//PMID", default="Unknown")
    
    return {
        "pmid": pmid,
        "title": title,
        "authors": authors,
        "year": year,
        "journal": journal,
        "abstract": abstract
    }
    
def parse_batch(xml_list):
    """Parse a list of XML abstracts, return list of clean dictionaries."""
    results = []
    for xml_text in xml_list:
        parsed = parse_abstract(xml_text)
        if parsed is not None:
            results.append(parsed)
        return results