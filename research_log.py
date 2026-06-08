#!/usr/bin/env python3

import json
import os
from datetime import datetime

LOG_PATH = os.path.expanduser("~/fringe-clinical/logs/research_log.jsonl")

def log_results(query, articles):
    """Log a search seasion and its results to JSONL."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "result_count": len(articles),
        "articles": articles
    }
    
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
        
    print(f"[LOG] {len(articles)} results saved for query: '{query}'")
    
def load_log():
    """Load all previous research sessions."""
    if not os.path.exists(LOG_PATH):
        print("[LOG] no research log found yet.")
        return []
    
    entries = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            entries.append(json.loads(line))
        return entries
    
def show_history():
    """Print a summary of all past searches."""
    entries = load_log()
    if not entries:
        return
    
    print("\n--- Research History ---")
    for entry in entries:
        print(f"{entry['timestamp']} | {entry['result_count']} results | {entry['query']}")
    print("-----------------------\n")