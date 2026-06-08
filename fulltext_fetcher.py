#!/usr/bin/env python3

import requests
import time
import os

UNPAYWALL_EMAIL = "fringe.clinical@localhost"
PMC_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def check_pmc(pmid):
    """Check if full text is available in PubMed Central."""
    url = PMC_BASE + "elink.fcgi"
    params = {
        "dbfrom": "pubmed",
        "db": "pmc",
        "id": pmid,
        "retmode": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        time.sleep(0.4)
        if response.status_code != 200:
            return None
        data = response.json()
        links = data["linksets"][0]["linksetdbs"][0]["links"]
        if links:
            pmc_id = links(0)
            return f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/"
    except Exception:
        return None
    
def check_unpaywall(doi):
    """Check unpaywall for legal free full text."""
    if not doi:
        return None
    
    url = f"https://api.unpaywall.org/v2/{doi}"
    params = {"email": UNPAYWALL_EMAIL}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        time.sleep(0.4)
        
        if response.status_code !=200:
            return None
        
        data = response.json()
        if data.get("isoa"):
            best = data.get("best_oa_location")
            if best:
                return best.get("url_for_pdf") or best.get("url")
    except Exception:
        return None
    
def find_fulltext(article):
    """Try PMC first, then unpaywall. Return best available URL."""
    pmid = article.get("pmid")
    doi = article.get("doi")
    
    pmc_url = check_pmc(pmid)
    if pmc_url:
        return {"source": "PMC", "url": pmc_url}
    
    oa_url = check_unpaywall(doi)
    if oa_url:
        return {"source": "Unpaywall", "url": oa_url}
    
    return {"source": "Abstract only", "url": article.get("url")}