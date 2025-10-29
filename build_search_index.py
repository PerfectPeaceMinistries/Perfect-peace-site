# build_search_index.py
import os, json, re
from glob import glob
from bs4 import BeautifulSoup

def extract_doc(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    title = (soup.title.string or '').strip() if soup.title else ''
    if not title:
        h = soup.select_one('h1,h2')
        title = h.get_text(strip=True) if h else os.path.basename(fp)
    article = soup.select_one('article')
    text = article.get_text(" ", strip=True) if article else soup.get_text(" ", strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    url = os.path.basename(fp)
    return {"title": title, "url": url, "excerpt": (text[:220] + ('…' if len(text) > 220 else ''))}

# adjust the glob if your posts live in subfolders:
files = glob("*.html") + glob("**/*.html", recursive=True)
# filter out pages you don't want indexed (e.g., admin, search itself)
skip = {"search.html", "blog.html", "doctrine-defined.html"}
docs = [extract_doc(fp) for fp in files if os.path.basename(fp) not in skip]

for i, d in enumerate(sorted(docs, key=lambda x: x["title"]), start=1):
    d["id"] = str(i)

with open("search-index.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)
print("Wrote search-index.json with", len(docs), "docs")
