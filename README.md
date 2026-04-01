# NLP Corpus Chatbot — Artificial Intelligence Domain:
A domain-specific NLP question-answering chatbot built using TF-IDF retrieval. 
This project demonstrates corpus creation from multiple web sources and retrieval-based question answering — no LLMs or AI APIs used.


## Project Overview:
This project collects textual data about **Artificial Intelligence** from multiple online sources, builds a structured JSON corpus, 
and uses **TF-IDF + Cosine Similarity** to answer natural language questions based only on the stored corpus.


## Features
- Web scraping from Wikipedia, blogs, and PDF documents
- Text preprocessing pipeline (cleaning, normalization)
- Structured JSON corpus with source metadata
- TF-IDF based retrieval chatbot
- Shows similarity scores and sources for every answer


## Tech Stack:
| Tool | Purpose |
|------|---------|
| Python | Core language |
| BeautifulSoup | Web scraping |
| PyMuPDF (fitz) | PDF text extraction |
| scikit-learn | TF-IDF vectorization |
| JSON | Corpus storage format |


## Project Structure:
```
nlp_chatbot/
│
├── step1_scraper.py       # Scrapes Wikipedia, blogs, and PDFs
├── step2_preprocess.py    # Cleans text and builds corpus.json
├── step3_chatbot.py       # TF-IDF chatbot with interactive loop
└── corpus.json            # Final structured corpus (9 entries)
```


## Data Sources:
| # | Source | Type | Topic |
|---|--------|------|-------|
| 1 | Wikipedia | Web page | Artificial Intelligence Overview |
| 2 | Wikipedia | Web page | Machine Learning |
| 3 | Wikipedia | Web page | Natural Language Processing |
| 4 | Towards Data Science | Blog | AI Applications in Industry |
| 5 | Towards Data Science | Blog | Risks and Ethics of AI |
| 6 | IBM Think | Blog | AI vs Traditional Programming |
| 7 | AI Overview Report | PDF | History of AI |
| 8 | AI Overview Report | PDF | Types of AI |
| 9 | AI Overview Report | PDF | Future of AI |



## Installation
```bash
pip install requests beautifulsoup4 scikit-learn pymupdf
```


## How to Run
```bash
# Step 1 — Scrape data from web sources
python step1_scraper.py
# Step 2 — Clean and build the corpus
python step2_preprocess.py
# Step 3 — Start the chatbot
python step3_chatbot.py
```


## TF-IDF stands for:
TF (Term Frequency) — how often a word appears in a document
IDF (Inverse Document Frequency) — how rare that word is across all documents


## How your chatbot works:
Your question is typed → converted into a TF-IDF vector (just numbers)
All 9 corpus documents are also stored as TF-IDF vectors
Cosine similarity is calculated between your question and every document
The document with the highest similarity score is returned as the answer


## Concepts Demonstrated
- Corpus creation from heterogeneous sources
- Web scraping for NLP datasets
- Text preprocessing and cleaning
- TF-IDF vectorization
- Cosine similarity based retrieval
- Retrieval-based question answering
