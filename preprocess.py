"""
Step 2 - Text Preprocessing & Corpus Builder
Reads raw scraped data, cleans it, and outputs a structured JSON corpus.
"""

import json
import re


# ─────────────────────────────────────────────
# PREPROCESSING PIPELINE
# ─────────────────────────────────────────────

def preprocess(text):
    """Apply a full preprocessing pipeline to raw text."""

    # Step 1: Lowercase (optional — keep original case for readability)
    # text = text.lower()

    # Step 2: Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Step 3: Remove citation markers like [1], [23]
    text = re.sub(r'\[\d+\]', '', text)

    # Step 4: Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?\'\"()-]', '', text)

    # Step 5: Collapse multiple whitespace
    text = re.sub(r'\s{2,}', ' ', text)

    # Step 6: Strip leading/trailing whitespace
    text = text.strip()

    return text


def build_corpus(raw_path, output_path):
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    corpus = []
    for idx, entry in enumerate(raw_data):
        cleaned_content = preprocess(entry.get("content", ""))

        if len(cleaned_content) < 50:
            print(f"  [Skip] Entry {idx} too short after cleaning.")
            continue

        corpus_entry = {
            "id": idx + 1,
            "source": entry.get("source", "Unknown"),
            "topic": entry.get("topic", "Unknown"),
            "content": cleaned_content
        }
        corpus.append(corpus_entry)
        print(f"  [OK] Entry {idx+1}: {entry['topic']} ({len(cleaned_content)} chars)")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print(f"\n[Done] Corpus with {len(corpus)} entries saved to {output_path}")
    return corpus


# ─────────────────────────────────────────────
# SAMPLE CORPUS (used if you don't have live scraped data)
# ─────────────────────────────────────────────

SAMPLE_CORPUS = [
    {
        "id": 1,
        "source": "Wikipedia",
        "topic": "Artificial Intelligence – Overview",
        "content": "Artificial intelligence is the simulation of human intelligence processes by machines, especially computer systems. AI research focuses on reasoning, knowledge representation, planning, learning, natural language processing, and perception. The field was founded in 1956 at a Dartmouth conference by John McCarthy, Marvin Minsky, and others."
    },
    {
        "id": 2,
        "source": "Wikipedia",
        "topic": "Machine Learning",
        "content": "Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that access data and use it to learn for themselves. Deep learning uses neural networks with many layers to model complex patterns in data."
    },
    {
        "id": 3,
        "source": "Wikipedia",
        "topic": "Natural Language Processing",
        "content": "Natural language processing (NLP) is a branch of AI concerned with giving computers the ability to understand text and spoken words. NLP combines computational linguistics with statistical, machine learning, and deep learning models. Applications include translation, sentiment analysis, and chatbots."
    },
    {
        "id": 4,
        "source": "Blog – Towards Data Science",
        "topic": "AI Applications in Industry",
        "content": "AI is widely used in healthcare for medical image diagnosis, drug discovery, and patient risk prediction. In finance, AI powers fraud detection, algorithmic trading, and credit scoring. Autonomous vehicles use AI for real-time object detection and path planning."
    },
    {
        "id": 5,
        "source": "Blog – Towards Data Science",
        "topic": "Risks and Ethics of AI",
        "content": "AI poses risks including job displacement due to automation, algorithmic bias in decisions, and potential misuse in surveillance. Ethical concerns involve lack of transparency in black-box models. Responsible AI development requires fairness, accountability, and explainability."
    },
    {
        "id": 6,
        "source": "Blog – IBM Think",
        "topic": "AI vs Traditional Programming",
        "content": "Traditional programming requires explicit rules coded by humans. AI learns rules from data instead. The shift from rule-based systems to data-driven models has enabled breakthroughs in image recognition, speech recognition, and game playing such as AlphaGo and GPT-based language models."
    },
    {
        "id": 7,
        "source": "PDF – AI Overview Report",
        "topic": "History of AI",
        "content": "The concept of artificial intelligence dates back to Alan Turing's 1950 paper Computing Machinery and Intelligence, which proposed the Turing Test. The 1956 Dartmouth workshop is considered the birth of AI as a field. AI went through several winters of reduced funding before the deep learning revolution of the 2010s."
    },
    {
        "id": 8,
        "source": "PDF – AI Overview Report",
        "topic": "Types of AI",
        "content": "AI can be classified into narrow AI, which performs specific tasks like image classification, and general AI, which can perform any intellectual task a human can. Reinforcement learning systems like AlphaZero learn through reward signals. Generative AI models such as GPT and DALL-E create new content from patterns learned in training data."
    },
    {
        "id": 9,
        "source": "PDF – AI Overview Report",
        "topic": "Future of AI",
        "content": "The future of AI includes advances in multimodal models that process text, images, and audio together. AI is expected to transform education, scientific research, and climate modeling. Key challenges include achieving AI safety, interpretability, and aligning AI systems with human values and societal goals."
    }
]


if __name__ == "__main__":
    import os

    if os.path.exists("corpus_raw.json"):
        print("[Mode] Building from scraped data...")
        build_corpus("corpus_raw.json", "corpus.json")
    else:
        print("[Mode] Using sample corpus (no scraped data found)...")
        with open("corpus.json", "w", encoding="utf-8") as f:
            json.dump(SAMPLE_CORPUS, f, indent=2, ensure_ascii=False)
        print(f"[Done] Sample corpus with {len(SAMPLE_CORPUS)} entries saved to corpus.json")