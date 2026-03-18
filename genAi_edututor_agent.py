"""
genAi_edututor_agent.py
-----------------------
Main AI Tutor Agent — Education Tutor for Remote India
Uses: Gemini 1.5 Flash (FREE tier) + Context Pruning

Run: python genAi_edututor_agent.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table
from rich import box

import google.generativeai as genai

from context_pruner import ContextPruner

# ──────────────────────────────────────────────
load_dotenv()
console = Console()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"   # FREE tier model — fast & capable

# System prompt for curriculum-aligned tutoring
SYSTEM_PROMPT = """You are EduTutor AI — a highly accurate, expert tutor for Indian school and university students (CBSE, ICSE, and State Board curriculum).

═══ ACCURACY RULES (highest priority) ═══
1. Read the [TEXTBOOK CONTEXT] carefully before answering. If the answer is in the context, use it as the primary source.
2. If the topic is NOT in the context, use your own deep knowledge. Say: "📌 General answer (not in loaded textbook):" before it.
3. NEVER guess or make up facts. For science/math: always include the correct formula, unit, and worked example.

═══ FORMAT RULES ═══
4. Structure every answer like this:
   **[Direct answer in one sentence]**
   **Explanation:** bullet points with detail
   **Example:** a real-life Indian example
   **Formula/Key fact:** (if applicable)
   💬 *Follow-up: one question to check understanding*
5. Use **bold** for key terms. Use bullet points. Simple English (Class 8–10 level).
6. Length: 180–380 words. NEVER truncate. Always finish the full answer.

═══ TONE ═══
7. Warm, encouraging, patient. Every question is a great question."""


def setup_gemini():
    """Configure Gemini API."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        console.print(Panel(
            "[bold red]❌ GEMINI_API_KEY not set![/bold red]\n\n"
            "Get your FREE key (no credit card needed):\n"
            "[link=https://aistudio.google.com/app/apikey]"
            "https://aistudio.google.com/app/apikey[/link]\n\n"
            "Then edit [yellow].env[/yellow] and set:\n"
            "[cyan]GEMINI_API_KEY=your_actual_key_here[/cyan]",
            title="Setup Required", border_style="red"
        ))
        sys.exit(1)

    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
        generation_config={
            "temperature": 0.4,        # Low temp for factual accuracy
            "max_output_tokens": 600,  # Keep responses short = low cost
            "top_p": 0.8,
        },
    )


def ask_tutor(model, pruner: ContextPruner, question: str) -> str:
    """
    Core function: Prune context → Build prompt → Call Gemini.
    """
    # Step 1: Context Pruning (the money-saver)
    context = pruner.build_context(question, top_k=4)

    # Step 2: Build minimal prompt
    prompt = f"""Below are the most relevant sections from the student's textbook (selected by Context Pruning):

[TEXTBOOK CONTEXT — use this as primary source]
{context}

[STUDENT QUESTION]
{question}

Instructions:
- If the answer is in the TEXTBOOK CONTEXT, base your answer on it.
- If NOT in the context, use your own knowledge and prefix with "📌 General answer (not in loaded textbook):"
- Follow the structured format. Complete the full answer — do not stop early."""

    # Step 3: Call Gemini (only ~2k tokens, not 100k!)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error calling Gemini API: {e}\nCheck your API key and internet connection."


def show_welcome():
    """Display welcome banner."""
    console.print(Panel(
        "[bold cyan]🎓 EduTutor AI — Education Tutor for Remote India[/bold cyan]\n"
        "[dim]Powered by Gemini 1.5 Flash (Free) + Context Pruning[/dim]\n\n"
        "📚 Ask any question from your textbook\n"
        "💡 Type [yellow]'topics'[/yellow] to see loaded subjects\n"
        "📖 Type [yellow]'ingest'[/yellow] to add a new PDF textbook\n"
        "🚪 Type [yellow]'quit'[/yellow] or [yellow]'exit'[/yellow] to leave",
        border_style="cyan",
        title="Welcome",
    ))


def show_topics(pruner: ContextPruner):
    """Display all available subjects/topics."""
    if not pruner.chunks:
        console.print("[yellow]No topics loaded. Add .txt files to _data/ or ingest a PDF.[/yellow]")
        return

    table = Table(title="📚 Loaded Topics", box=box.ROUNDED, border_style="cyan")
    table.add_column("Subject", style="bold green")
    table.add_column("Topic / Chapter", style="cyan")
    table.add_column("Words", style="dim")
    table.add_column("File", style="dim")

    for chunk in pruner.chunks[:30]:  # Show max 30
        table.add_row(
            chunk.get("subject", "Unknown")[:30],
            chunk.get("title", "N/A")[:40],
            str(len(chunk.get("text", "").split())),
            chunk.get("filename", "")[:30],
        )

    console.print(table)


def ingest_mode():
    """Interactive PDF ingestion."""
    from pdf_ingestor import ingest_pdf
    pdf_path = Prompt.ask("[cyan]Enter path to PDF textbook[/cyan]")
    subject = Prompt.ask("[cyan]Enter subject name (e.g. 'Class 10 Science')[/cyan]")
    ingest_pdf(pdf_path, subject)
    console.print("[green]✅ PDF ingested! Restart the tutor to load new content.[/green]")


def main():
    show_welcome()

    # Load model
    console.print("[dim]🔧 Setting up Gemini...[/dim]")
    model = setup_gemini()
    console.print(f"[green]✅ Connected to {MODEL_NAME}[/green]\n")

    # Load context pruner
    pruner = ContextPruner()

    if not pruner.chunks:
        console.print(Panel(
            "[yellow]⚠ No textbook data found in [bold]_data/[/bold]\n\n"
            "To get started:\n"
            "1. Add .txt topic files to the [bold]_data/[/bold] folder, OR\n"
            "2. Type [cyan]'ingest'[/cyan] to process a PDF textbook\n\n"
            "Sample data files are included — try asking about them!",
            border_style="yellow"
        ))

    # Chat loop
    chat_history = []
    console.print()

    while True:
        try:
            question = Prompt.ask("[bold green]You[/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye! Keep learning! 📚[/dim]")
            break

        if not question:
            continue

        cmd = question.lower()

        if cmd in ("quit", "exit", "bye"):
            console.print("[dim]Goodbye! Keep learning! 📚[/dim]")
            break

        elif cmd == "topics":
            show_topics(pruner)
            continue

        elif cmd == "ingest":
            ingest_mode()
            pruner = ContextPruner()  # Reload with new data
            continue

        elif cmd == "clear":
            chat_history.clear()
            console.print("[dim]Chat history cleared.[/dim]")
            continue

        # Get answer
        with console.status("[cyan]🤔 Thinking...[/cyan]"):
            answer = ask_tutor(model, pruner, question)

        console.print()
        console.print(Panel(
            Markdown(answer),
            title="[bold cyan]🤖 EduTutor[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        ))
        console.print()

        # Store in history (optional, for context)
        chat_history.append({"q": question, "a": answer})


if __name__ == "__main__":
    main()
