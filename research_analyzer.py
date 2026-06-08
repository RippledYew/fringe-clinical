#!/usr/bin/env python3

import json
import os
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

LOG_PATH = os.path.expanduser("~/fringe-clinical/logs/research_log.jsonl")

def load_articles():
    """Load all articles from research log."""
    if not os.path.exists(LOG_PATH):
        console.print("[red] No research log found. Run some searches first.[/red]")
        return []
    
    articles = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            entry = json.loads(line)
            for article in entry.get("articles", []):
                article["query"] = entry.get("query", "")
                articles.append(article)
    return articles

def analyze(articles):
    """Run sklearn analysis on article library."""
    if len(articles) < 2:
        console.print("[yellow]Need at least two articles to analyze. run more searches first.[/yellow]")
        
    abstracts = [a.get("abstract", "") for a in articles]
    titles = [a.get("title", "Unknown") for a in articles]
    journals = [a.get("jorunal", "Unknown") for a in articles]
    years = [a.get("year", "Unknown") for a in articles]
    
    #TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english", max_features=100)
    X = vectorizer.fit_transform(abstracts)
    terms = vectorizer.get_feature_names_out()
    
    #KMeans clusters
    n_clusters = min(3, len(articles))
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    km.fit(X)
    labels = km.labels_
    
    # --- Cluster Report ---
    console.print(Panel("[bold cyan]Topic CLusters[/bold cyan]"))
    for i in range(n_clusters):
        cluster_articles = [titles[j] for j in range(len(titles)) if labels[j] == i]
        top_terms_idx = km.cluster_centers_[i].argsort()[-5:][::-1]
        top_terms = [terms[idx] for idx in top_terms_idx]
        
        table = Table(title=f"Cluster {i+1}: {', '.join(top_terms)}")
        table.add_column("Articles", style="white")
        for title in cluster_articles:
            table.add_row(title[:80])
        console.print(table)
        
    # --- Journal Frequency ---
    console.print(Panel("[bold cyan]Most Active Journals[/bold cyan]"))
    journal_counts = Counter(journals).most_common(5)
    jt = Table()
    jt.add_column("Journal", style="green")
    jt.add_column("Count", style="yellow")
    for journal, count in journal_counts:
        jt.add_row(journal[:60], str(count))
    console.print(jt)
    
    # --- Year Trend ---
    console.print(Panel("[bold cyan]Publication Year Trend[/bold cyan]"))
    year_counts = Counter(years).most_common()
    year_counts.sort()
    yt = Table()
    yt.add_column("Year", style="green")
    yt.add_column("Papers", style="yellow")
    for year, count in year_counts:
        yt.add_row(str(year), str(count))
    console.print(yt)
    
    console.print(f"\n[bold green]Total articles analyzed: {len(articles)}[/bold green]\n")
    
def run_analysis():
    articles = load_articles()
    if articles:
        analyze(articles)