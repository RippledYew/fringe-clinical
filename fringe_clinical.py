#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subprocess
from pubmed_query import search_pubmed, fetch_abstracts_batch
from abstract_parser import parse_batch
from research_log import log_results, show_history
from research_analyzer import run_analysis
from fulltext_fetcher import find_fulltext

def banner():
    os.system("figlet -f slant 'Fringe Clinical' | lolcat")
              
def run_search():
    query = input("\nEnter research query: ")
    print("\nSearching PubMed...\n")

    ids = search_pubmed(query, 5)
    raw = fetch_abstracts_batch(ids)
    articles = parse_batch(raw)
    
    for article in articles:
        print(f"PMID: {article['pmid']}")
        print(f"Title: {article['title']}")
        print(f"Journal: {article['journal']}")
        print(f"year: {article['year']}")
        print(f"Authors: {', '.join(article['authors'][:3])}")
        print(f"Abstract:{article['abstract'][:400]}")
        fulltext = find_fulltext(article)
        print(f"Full Text ({fulltext['source']}): {fulltext['url']}")
        print("-" * 60)
        
    log_results(query, articles)
    
def main():
    banner()
    while True:
        print("\n[ Fringe Clinical ]")
        print("1. Search PubMed")
        print("2. Research History")
        print("3. Analyze My Research")
        print("4. Exit")
        
        choice = input("\nSelect: ")
        
        if choice == "1":
            run_search()
        elif choice == "2":
            show_history()
        elif choice == "3":
            run_analysis()
        elif choice == "4":
            print("\nGoodnight")
            break
        
if __name__ == "__main__":
    main()