"""
pdf_ingestor.py
--------------
Ingests large PDF textbooks, splits them into chapter/topic chunks,
and saves them as structured .txt files in the _data/ directory.
Run this ONCE per textbook — never re-process on every query.
"""

import os
import re
import json
import PyPDF2
from pathlib import Path
from rich.console import Console
from rich.progress import track

console = Console()

DATA_DIR = Path("_data")
DATA_DIR.mkdir(exist_ok=True)


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text page by page from a PDF."""
    pages = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        total = len(reader.pages)
        console.print(f"[cyan]📖 Found {total} pages in PDF...[/cyan]")
        for i, page in enumerate(track(reader.pages, description="Extracting pages")):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                pages.append({"page": i + 1, "text": text})
    return pages


def detect_chapters(pages: list[dict]) -> list[dict]:
    """
    Detect chapter boundaries using common heading patterns.
    Groups pages into chapters for Context Pruning later.
    """
    chapter_pattern = re.compile(
        r"^(chapter\s+\d+|unit\s+\d+|section\s+\d+|\d+\.\s+[A-Z])",
        re.IGNORECASE | re.MULTILINE,
    )

    chunks = []
    current_chunk = {"title": "Introduction", "pages": [], "text": ""}

    for page_data in pages:
        text = page_data["text"]
        lines = text.split("\n")
        first_line = lines[0].strip() if lines else ""

        # Check if this page starts a new chapter
        if chapter_pattern.match(first_line) and current_chunk["text"]:
            # Save current chunk
            chunks.append(current_chunk)
            current_chunk = {
                "title": first_line[:80],  # truncate long titles
                "pages": [page_data["page"]],
                "text": text,
            }
        else:
            current_chunk["pages"].append(page_data["page"])
            current_chunk["text"] += "\n\n" + text

    # Add the last chunk
    if current_chunk["text"]:
        chunks.append(current_chunk)

    return chunks


def merge_small_chunks(chunks: list[dict], min_words: int = 200) -> list[dict]:
    """Merge tiny chunks into neighbours to avoid too-small context windows."""
    merged = []
    buffer = None

    for chunk in chunks:
        word_count = len(chunk["text"].split())
        if word_count < min_words:
            if buffer:
                buffer["text"] += "\n\n" + chunk["text"]
                buffer["pages"].extend(chunk["pages"])
            else:
                buffer = chunk
        else:
            if buffer:
                buffer["text"] += "\n\n" + chunk["text"]
                buffer["pages"].extend(chunk["pages"])
                merged.append(buffer)
                buffer = None
            else:
                merged.append(chunk)

    if buffer:
        merged.append(buffer)

    return merged


def save_chunks(chunks: list[dict], subject_name: str):
    """
    Save each chunk as finalDataset.<subject>.txt
    Also saves a manifest JSON for fast lookup.
    """
    safe_name = subject_name.lower().replace(" ", "_")
    manifest = []

    for idx, chunk in enumerate(chunks):
        filename = f"finalDataset.{safe_name}.chunk{idx:03d}.txt"
        filepath = DATA_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"SUBJECT: {subject_name}\n")
            f.write(f"CHUNK_ID: {idx}\n")
            f.write(f"TITLE: {chunk['title']}\n")
            f.write(f"PAGES: {chunk['pages']}\n")
            f.write(f"WORD_COUNT: {len(chunk['text'].split())}\n")
            f.write("=" * 60 + "\n")
            f.write(chunk["text"])

        manifest.append(
            {
                "chunk_id": idx,
                "title": chunk["title"],
                "pages": chunk["pages"],
                "filename": filename,
                "word_count": len(chunk["text"].split()),
            }
        )

    manifest_path = DATA_DIR / f"manifest.{safe_name}.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    console.print(
        f"[green]✅ Saved {len(chunks)} chunks for '{subject_name}'[/green]"
    )
    console.print(f"[green]📋 Manifest: {manifest_path}[/green]")
    return manifest_path


def ingest_pdf(pdf_path: str, subject_name: str = None):
    """Main entry point: ingest a PDF textbook."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        console.print(f"[red]❌ File not found: {pdf_path}[/red]")
        return

    if not subject_name:
        subject_name = pdf_path.stem.replace("_", " ").title()

    console.print(f"\n[bold yellow]📚 Ingesting: {pdf_path.name}[/bold yellow]")
    console.print(f"[yellow]Subject: {subject_name}[/yellow]\n")

    pages = extract_text_from_pdf(str(pdf_path))
    console.print(f"[cyan]🔍 Detecting chapters...[/cyan]")
    chunks = detect_chapters(pages)
    chunks = merge_small_chunks(chunks)
    console.print(f"[cyan]📦 Created {len(chunks)} topic chunks[/cyan]")
    save_chunks(chunks, subject_name)

    console.print(
        f"\n[bold green]🎉 Ingestion complete! "
        f"{len(pages)} pages → {len(chunks)} smart chunks[/bold green]"
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        console.print("[bold]Usage:[/bold] python pdf_ingestor.py <path_to_pdf> [subject_name]")
        console.print("[dim]Example: python pdf_ingestor.py textbook.pdf 'Class 10 Science'[/dim]")
    else:
        pdf = sys.argv[1]
        subject = sys.argv[2] if len(sys.argv) > 2 else None
        ingest_pdf(pdf, subject)
