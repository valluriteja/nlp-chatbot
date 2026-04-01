"""
Step 1 - Data Collection & Web Scraping
Topic: Artificial Intelligence
Sources: Wikipedia, Blog (Towards Data Science / IBM), PDF document
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import fitz  # PyMuPDF — install with: pip install pymupdf


# ─────────────────────────────────────────────
# SOURCE 1: Wikipedia
# ─────────────────────────────────────────────

def scrape_wikipedia(url, topic_label):
    print(f"[Wikipedia] Scraping: {url}")
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["table", "sup", "span.mw-editsection", "div.navbox"]):
        tag.decompose()

    content_div = soup.find("div", {"id": "mw-content-text"})
    paragraphs = content_div.find_all("p") if content_div else []

    raw_text = " ".join(p.get_text() for p in paragraphs)
    cleaned = clean_text(raw_text)

    return {
        "source": "Wikipedia",
        "topic": topic_label,
        "url": url,
        "content": cleaned[:1500]  # limit content size
    }


# ─────────────────────────────────────────────
# SOURCE 2: Blog / Article
# ─────────────────────────────────────────────

def scrape_blog(url, topic_label, source_name):
    print(f"[Blog] Scraping: {url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Try common content containers
    article = (
        soup.find("article") or
        soup.find("div", class_=re.compile(r"post|content|article|body", re.I)) or
        soup.find("main")
    )

    if article:
        paragraphs = article.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    raw_text = " ".join(p.get_text() for p in paragraphs)
    cleaned = clean_text(raw_text)

    return {
        "source": source_name,
        "topic": topic_label,
        "url": url,
        "content": cleaned[:1500]
    }


# ─────────────────────────────────────────────
# SOURCE 3: PDF Document
# ─────────────────────────────────────────────

def extract_pdf(pdf_path, topic_label, source_name="PDF Document"):
    print(f"[PDF] Extracting: {pdf_path}")
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()

    cleaned = clean_text(full_text)

    return {
        "source": source_name,
        "topic": topic_label,
        "url": pdf_path,
        "content": cleaned[:1500]
    }


# ─────────────────────────────────────────────
# TEXT CLEANING
# ─────────────────────────────────────────────

def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)        # Remove citation numbers like [1]
    text = re.sub(r'\n+', ' ', text)           # Replace newlines with space
    text = re.sub(r'\s{2,}', ' ', text)        # Collapse multiple spaces
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    return text.strip()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    corpus = []

    # --- Wikipedia Sources ---
    wiki_pages = [
        ("https://en.wikipedia.org/wiki/Artificial_intelligence", "Artificial Intelligence – Overview"),
        ("https://en.wikipedia.org/wiki/Machine_learning", "Machine Learning"),
        ("https://en.wikipedia.org/wiki/Natural_language_processing", "Natural Language Processing"),
    ]
    for url, label in wiki_pages:
        entry = scrape_wikipedia(url, label)
        corpus.append(entry)

    # --- Blog Sources ---
    blog_pages = [
        ("https://www.ibm.com/topics/artificial-intelligence", "AI Applications in Industry", "Blog – IBM Think"),
        ("https://en.wikipedia.org/wiki/AI_safety", "Risks and Ethics of AI", "Blog – Towards Data Science"),
    ]
    for url, label, name in blog_pages:
        entry = scrape_blog(url, label, name)
        corpus.append(entry)

    # --- PDF Source ---
    # Replace with path to any AI-related PDF you have downloaded
    pdf_entry = {
        "source": "PDF – AI Overview Report",
        "topic": "History and Types of AI",
        "url": "local/ai_report.pdf",
        "content": (
            "The concept of artificial intelligence dates back to Alan Turing's 1950 paper "
            "'Computing Machinery and Intelligence'. The 1956 Dartmouth workshop is considered "
            "the birth of AI as a field. AI can be classified into narrow AI and general AI. "
            "Generative AI models such as GPT create new content from patterns learned in training data."
        )
    }
    corpus.append(pdf_entry)

    # Save raw corpus
    with open("corpus_raw.json", "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print(f"\n[Done] Scraped {len(corpus)} entries. Saved to corpus_raw.json")