"""
context_pruner.py
-----------------
THE CORE COST-SAVING MODULE — Context Pruning

Instead of sending the ENTIRE textbook to Gemini on every query,
this module finds only the most relevant chunks and sends those.

Cost comparison:
  ❌ Naive RAG:    Full book (~100k tokens) per query  → expensive
  ✅ Context Pruning: Top 3-5 chunks (~2k tokens) per query → 98% cheaper
"""

import os
import json
import math
import re
from pathlib import Path
from collections import Counter

from rich.console import Console

console = Console()
DATA_DIR = Path("_data")


# ──────────────────────────────────────────────
# 1.  Simple TF-IDF based retrieval (no paid embeddings!)
# ──────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """Lowercase, remove punctuation, split."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [w for w in text.split() if len(w) > 2]


def build_tf(tokens: list[str]) -> dict:
    count = Counter(tokens)
    total = len(tokens) if tokens else 1
    return {word: freq / total for word, freq in count.items()}


def cosine_similarity(tf1: dict, tf2: dict) -> float:
    """Dot product / (|a| * |b|) between two TF vectors."""
    common = set(tf1) & set(tf2)
    dot = sum(tf1[w] * tf2[w] for w in common)
    mag1 = math.sqrt(sum(v ** 2 for v in tf1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in tf2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


# ──────────────────────────────────────────────
# 2.  Chunk loader
# ──────────────────────────────────────────────

def load_all_chunks(subject_filter: str = None) -> list[dict]:
    """
    Load all saved .txt chunks from _data/.
    Optionally filter by subject name.
    """
    chunks = []
    pattern = "finalDataset.*.chunk*.txt"

    for filepath in sorted(DATA_DIR.glob(pattern)):
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        # Parse header
        lines = raw.split("\n")
        meta = {}
        text_start = 0
        for i, line in enumerate(lines):
            if line.startswith("SUBJECT:"):
                meta["subject"] = line.split(":", 1)[1].strip()
            elif line.startswith("CHUNK_ID:"):
                meta["chunk_id"] = line.split(":", 1)[1].strip()
            elif line.startswith("TITLE:"):
                meta["title"] = line.split(":", 1)[1].strip()
            elif line.startswith("PAGES:"):
                meta["pages"] = line.split(":", 1)[1].strip()
            elif "=" * 20 in line:
                text_start = i + 1
                break

        body = "\n".join(lines[text_start:]).strip()
        meta["text"] = body
        meta["filename"] = filepath.name

        if subject_filter:
            if subject_filter.lower() in meta.get("subject", "").lower():
                chunks.append(meta)
        else:
            chunks.append(meta)

    return chunks


def load_plain_txt_chunks(subject_filter: str = None) -> list[dict]:
    """
    Load plain .txt data files (like the reference project's
    finalDataset0.2.exam.txt style) as single chunks.
    """
    chunks = []
    simple_patterns = [
        "finalDataset*.txt",
        "hostel_rules*.txt",
        "new.finalDataset*.txt",
        "report.txt",
    ]
    seen = set()

    for pattern in simple_patterns:
        for filepath in DATA_DIR.glob(pattern):
            if filepath.name in seen or "chunk" in filepath.name:
                continue
            seen.add(filepath.name)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if not text:
                continue
            subject = filepath.stem.replace("finalDataset0.2.", "").replace("_", " ").title()
            if subject_filter and subject_filter.lower() not in subject.lower():
                continue
            chunks.append({
                "subject": subject,
                "chunk_id": "0",
                "title": subject,
                "pages": "N/A",
                "text": text,
                "filename": filepath.name,
            })

    return chunks


# ──────────────────────────────────────────────
# 3.  Context Pruner (main API)
# ──────────────────────────────────────────────

class ContextPruner:
    """
    Retrieves the top-k most relevant chunks for a query
    WITHOUT calling any external API — pure local TF-IDF.
    """

    def __init__(self, subject_filter: str = None):
        self.chunks = load_all_chunks(subject_filter)
        # Also load plain txt files
        self.chunks.extend(load_plain_txt_chunks(subject_filter))

        if not self.chunks:
            console.print(
                "[yellow]⚠ No data chunks found in _data/. "
                "Run pdf_ingestor.py first, or add .txt files to _data/[/yellow]"
            )
        else:
            console.print(
                f"[dim]🗂  Loaded {len(self.chunks)} chunks from {DATA_DIR}/[/dim]"
            )

        # Pre-compute TF for all chunks
        self._chunk_tfs = [
            build_tf(tokenize(c["text"])) for c in self.chunks
        ]

    def prune(self, query: str, top_k: int = 4) -> list[dict]:
        """
        Return the top_k most relevant chunks for the query.
        This is Context Pruning — we only send these to Gemini.
        """
        if not self.chunks:
            return []

        query_tf = build_tf(tokenize(query))
        scores = [
            cosine_similarity(query_tf, chunk_tf)
            for chunk_tf in self._chunk_tfs
        ]

        # Get top_k indices
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, score in ranked[:top_k] if score > 0]

        # Fall back to top chunks even if score is 0
        if not top_indices:
            top_indices = [idx for idx, _ in ranked[:top_k]]

        pruned = [self.chunks[i] for i in top_indices]

        # Log cost savings estimate
        total_words = sum(len(c["text"].split()) for c in self.chunks)
        pruned_words = sum(len(c["text"].split()) for c in pruned)
        if total_words > 0:
            savings = (1 - pruned_words / total_words) * 100
            console.print(
                f"[dim]✂  Context Pruning: sending {pruned_words:,} / {total_words:,} "
                f"words ({savings:.0f}% tokens saved)[/dim]"
            )

        return pruned

    def build_context(self, query: str, top_k: int = 4) -> str:
        """Return a formatted context string ready to inject into a prompt."""
        relevant_chunks = self.prune(query, top_k)
        if not relevant_chunks:
            return "No relevant textbook content found."

        parts = []
        for chunk in relevant_chunks:
            header = (
                f"[Source: {chunk.get('subject','Unknown')} | "
                f"Topic: {chunk.get('title','N/A')} | "
                f"Pages: {chunk.get('pages','N/A')}]"
            )
            # Limit each chunk to ~800 words to stay within token budget
            words = chunk["text"].split()
            body = " ".join(words[:800])
            if len(words) > 800:
                body += " ..."
            parts.append(f"{header}\n{body}")

        return "\n\n---\n\n".join(parts)
