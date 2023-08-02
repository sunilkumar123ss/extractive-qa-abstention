"""Sentence extraction with explicit lexical confidence and abstention."""
import argparse
import json
from pathlib import Path
import re

STOP = set("a an the is are was were do does did what which who how where when why of to in for and or be can with it".split())

def terms(text):
    return set(re.findall(r"\w+", text.casefold())) - STOP

