import re
import tkinter as tk
from tkinter import messagebox
from collections import Counter

from doc_task.summary_helper import append_summary_to_doc

_summarizer_pipeline = None


def _get_pipeline():
    """
    Lazy singleton loader for the T5 summarizer pipeline.
    Loads on first execution to ensure zero delay on app startup.
    """
    global _summarizer_pipeline
    if _summarizer_pipeline is None:
        try:
            print("[INFO] Initializing lightweight T5 summarization model...")
            from transformers import pipeline
            _summarizer_pipeline = pipeline(
                "summarization",
                model="google-t5/t5-small",
                tokenizer="google-t5/t5-small"
            )
            print("[INFO] T5 summarization model ready.")
        except Exception as e:
            print(f"[WARNING] Could not initialize Transformers T5 pipeline ({e}). Using native fallback engine.")
            _summarizer_pipeline = "FALLBACK"
    return _summarizer_pipeline


def _fallback_extractive_summary(text: str, max_sentences: int = 3) -> str:
    """
    Ultra-fast native extractive summarizer fallback (0-dependency).
    Used if deep learning dependencies are unavailable or offline.
    """
    stopwords = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
        "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
        "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from",
        "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
        "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
        "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
        "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
        "she", "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them",
        "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too",
        "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which",
        "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself"
    }
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 10]
    if len(sentences) <= max_sentences:
        return text

    words = re.findall(r'\w+', text.lower())
    meaningful = [w for w in words if w not in stopwords and len(w) > 2]
    freq = Counter(meaningful)
    max_freq = max(freq.values()) if freq else 1
    weights = {w: count / max_freq for w, count in freq.items()}

    scores = []
    for idx, sentence in enumerate(sentences):
        sentence_words = re.findall(r'\w+', sentence.lower())
        if not sentence_words:
            continue
        score = sum(weights.get(w, 0) for w in sentence_words) / len(sentence_words)
        if idx == 0:
            score *= 1.3
        elif idx == len(sentences) - 1:
            score *= 1.1
        scores.append((score, idx, sentence))

    scores.sort(key=lambda x: x[0], reverse=True)
    top = sorted(scores[:max_sentences], key=lambda x: x[1])
    return " ".join([s[2] for s in top])


def generate_summary(text: str) -> str:
    """
    Generate an abstractive summary of the given text using T5.
    """
    clean_text = text.strip()
    words = clean_text.split()
    
    # If text is very short, return as-is
    if len(words) <= 20:
        return clean_text

    pipeline_instance = _get_pipeline()
    if pipeline_instance == "FALLBACK" or pipeline_instance is None:
        return _fallback_extractive_summary(clean_text)

    try:
        # T5 standard summarization prefix
        input_prompt = f"summarize: {clean_text}"
        
        # Determine dynamic output constraints
        input_len = len(words)
        max_len = max(30, min(120, int(input_len * 0.6)))
        min_len = max(15, min(40, int(input_len * 0.25)))

        result = pipeline_instance(
            input_prompt,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            truncation=True
        )
        if result and len(result) > 0:
            return result[0].get("summary_text", "").strip()
        return _fallback_extractive_summary(clean_text)
    except Exception as err:
        print(f"[WARNING] T5 inference exception ({err}). Using fallback engine.")
        return _fallback_extractive_summary(clean_text)


def handle_summary_from_text(app_data, text: str):
    """
    Main handler for the Summary feature:
    1. Validates selected text
    2. Runs T5 abstractive summarization
    3. Appends formatted summary into current document
    4. Shows confirmation feedback
    """
    query = text.strip()
    if not query:
        messagebox.showwarning("No Text", "Please highlight text to summarize first!")
        return

    if len(query.split()) < 10:
        messagebox.showwarning(
            "Text Too Short",
            "Selected text is too short for summarization. Please select at least a sentence or paragraph."
        )
        return

    try:
        summary_result = generate_summary(query)
        if not summary_result:
            messagebox.showwarning("Summary Failed", "Could not generate a summary for the selected text.")
            return

        append_summary_to_doc(app_data, summary_result, original_preview=query[:60])
        messagebox.showinfo("Success", "Summary appended directly to your notes!")
    except Exception as e:
        messagebox.showerror("Summary Error", f"Failed to append summary:\n{e}")
