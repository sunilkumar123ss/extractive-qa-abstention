"""Sentence extraction with explicit lexical confidence and abstention."""
import argparse
import json
from pathlib import Path
import re

STOP = set("a an the is are was were do does did what which who how where when why of to in for and or be can with it".split())

def terms(text):
    return set(re.findall(r"\w+", text.casefold())) - STOP


def answer(question, sources, threshold=0.6):
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be in [0, 1]")
    if not isinstance(sources, dict) or not all(isinstance(k,str) and isinstance(v,str) for k,v in sources.items()):
        raise ValueError("sources must map IDs to text")
    query = terms(question)
    candidates = []
    if query:
        for source_id, text in sources.items():
            for index, sentence in enumerate(re.split(r"(?<=[.!?])\s+", text.strip())):
                overlap = query & terms(sentence)
                coverage = len(overlap) / len(query)
                if overlap and coverage >= threshold:
                    candidates.append((coverage, source_id, index, sentence, sorted(overlap)))
    if not candidates:
        return {"abstained": True, "answer": None, "source_id": None, "reason": "insufficient_lexical_evidence"}
    coverage, source, index, sentence, matched = sorted(candidates, key=lambda x: (-x[0], x[1], x[2]))[0]
    return {"abstained": False, "answer": sentence, "source_id": source,
            "sentence_index": index, "lexical_coverage": round(coverage, 4), "matched_terms": matched}

