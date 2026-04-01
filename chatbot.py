"""
Step 3 - Mini Chatbot using TF-IDF Retrieval
Accepts natural language questions and retrieves answers from the corpus.

Install dependencies:
    pip install scikit-learn
"""

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ─────────────────────────────────────────────
# LOAD CORPUS
# ─────────────────────────────────────────────

def load_corpus(path="corpus.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────────────────────────
# TF-IDF ENGINE
# ─────────────────────────────────────────────

class TFIDFChatbot:
    def __init__(self, corpus):
        self.corpus = corpus

        # Combine topic + content for better matching
        self.documents = [
            f"{entry['topic']} {entry['content']}" for entry in corpus
        ]

        # Build TF-IDF matrix
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),   # unigrams and bigrams
            max_df=0.85,
            min_df=1
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
        print(f"[Chatbot] Loaded {len(corpus)} documents into TF-IDF index.")
        print(f"[Chatbot] Vocabulary size: {len(self.vectorizer.vocabulary_)}")

    def answer(self, query, top_k=2, threshold=0.05):
        """Find the best matching documents and generate a response."""
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Get top-k results above threshold
        ranked_indices = np.argsort(similarities)[::-1]
        top_indices = [i for i in ranked_indices[:top_k] if similarities[i] >= threshold]

        if not top_indices:
            return {
                "answer": "I could not find a relevant answer in the corpus. Please try rephrasing your question or ask about AI topics.",
                "sources": [],
                "scores": []
            }

        # Build answer from top matches
        answer_parts = []
        sources = []

        for idx in top_indices:
            doc = self.corpus[idx]
            answer_parts.append(doc["content"])
            sources.append({
                "source": doc["source"],
                "topic": doc["topic"],
                "score": round(float(similarities[idx]), 4)
            })

        final_answer = " ".join(answer_parts)

        # Truncate to ~400 words for readability
        words = final_answer.split()
        if len(words) > 400:
            final_answer = " ".join(words[:400]) + "..."

        return {
            "answer": final_answer,
            "sources": sources,
            "scores": [s["score"] for s in sources]
        }


# ─────────────────────────────────────────────
# COMMAND-LINE CHATBOT LOOP
# ─────────────────────────────────────────────

def run_chatbot():
    corpus = load_corpus("corpus.json")
    bot = TFIDFChatbot(corpus)

    print("\n" + "="*60)
    print("  AI Domain Chatbot — TF-IDF Retrieval System")
    print("  Topic: Artificial Intelligence")
    print("  Type 'quit' to exit")
    print("="*60 + "\n")

    sample_questions = [
       
      "Who invented AI?",
      "What are the risks of AI?",
      "What is NLP?"
    ]

    print("Sample questions you can try:")
    for q in sample_questions:
        print(f"  • {q}")
    print()

    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() in ("quit", "exit", "bye"):
            print("Chatbot: Goodbye!")
            break

        result = bot.answer(query)

        print(f"\nChatbot: {result['answer']}\n")
        print("Sources used:")
        for s in result["sources"]:
            print(f"  [{s['score']:.4f}] {s['source']} — {s['topic']}")
        print()


# ─────────────────────────────────────────────
# DEMO — Run sample queries automatically
# ─────────────────────────────────────────────

def run_demo():
    corpus = load_corpus("corpus.json")
    bot = TFIDFChatbot(corpus)

    demo_queries = [
        "What are the main applications of Artificial Intelligence?",
        "What is machine learning and how does it work?",
        "What are the ethical risks of AI?",
        "Who invented artificial intelligence?",
        "What is the future of AI?"
    ]

    print("\n" + "="*60)
    print("  DEMO — Sample Queries & Answers")
    print("="*60)

    for query in demo_queries:
        print(f"\nQ: {query}")
        result = bot.answer(query)
        print(f"A: {result['answer'][:300]}...")
        for s in result["sources"]:
            print(f"   Source: {s['source']} | Topic: {s['topic']} | Score: {s['score']}")
        print("-"*60)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        run_chatbot()