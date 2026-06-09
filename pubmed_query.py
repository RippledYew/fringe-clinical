#!/usr/bin/env python3

import requests
import json
import time
import os

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query, max_results=20):
    """Search PubMed and return a list of article IDs."""
    search_url = BASE_URL + "esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    
    response = requests.get(search_url, params=params)
    time.sleep(0.4)
    try:
        data = response.json()
        return data["esearchresult"]["idlist"]
    except Exception:
        return []

def fetch_abstract(pubmed_id):
    """Fetch abstract text for a given PubMed ID."""
    fetch_url = BASE_URL + "efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "xml",
        "rettype": "abstract"
    }
    response = requests.get(fetch_url, params=params)
    time.sleep(0.4)
    if response.status_code == 200:
        return response.text
    else:
        return None
    
def fetch_abstracts_batch(id_list):
    """Fetch abstracts for a list of PubMEd IDs."""
    if not id_list:
        return []
    abstracts = []
    for pubmed_id in id_list:
        result = fetch_abstract(pubmed_id)
        if result is not None:
            abstracts.append(result)
        return abstracts
    