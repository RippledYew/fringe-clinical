from pubmed_query import search_pubmed, fetch_abstracts_batch
from abstract_parser import parse_batch

ids = search_pubmed("PFAS health outcomes", 3)
raw = fetch_abstracts_batch(ids)
articles = parse_batch(raw)

for article in articles:
    print(f"PMID: {article['pmid']}")
    print(f"Title: {article['title']}")
    print(f"JournalL {article['journal']}")
    print(f"Year: {article['year']}")
    print(f"Authors: {', '.join(article['authors'][:3])}")
    print(f"Abstract: {article['abstract'][:300]}")
    print("-" * 60)
