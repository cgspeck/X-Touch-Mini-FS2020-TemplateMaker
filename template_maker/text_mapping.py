
from dataclasses import dataclass
from pathlib import Path
from re import Pattern
import re
from typing import List

from template_maker.vars import default_mappings, user_mappings

@dataclass
class TextMapping:
    pat: Pattern
    replacement: str

def _from_disk(fp: Path) -> List[TextMapping]:
    memo = []

    txt =  fp.read_text()
    for l in txt.split("\n"):
        l = l.strip()
        if len(l) == 0:
            continue

        if l.startswith("#"):
            continue

        k, v = l.split("=")
        k = k.strip()
        v = v.strip()
        memo.append(TextMapping(
            pat=re.compile(k),
            replacement=v
        ))
    return memo

def load_mappings() -> List[TextMapping]:
    memo = []

    memo.extend(_from_disk(user_mappings))
    memo.extend(_from_disk(default_mappings))

    return memo