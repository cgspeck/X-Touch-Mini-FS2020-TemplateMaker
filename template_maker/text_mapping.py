import html
import re
from dataclasses import dataclass
from pathlib import Path
from re import Pattern
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin

from template_maker.vars import default_mappings, user_mappings


@dataclass
class TextMapping(DataClassJsonMixin):
    pat: Pattern
    replacement: str


def sanitise_replacement(original: str) -> str:
    return html.escape(original)


def _from_disk(fp: Path) -> List[TextMapping]:
    memo = []

    txt = fp.read_text()
    for l in txt.split("\n"):
        l = l.strip()
        if len(l) == 0:
            continue

        if l.startswith("#"):
            continue

        k, v = l.split("=")
        k = k.strip()
        v = v.strip()
        memo.append(TextMapping(pat=re.compile(k), replacement=sanitise_replacement(v)))
    return memo


def load_mappings(remove_unrecognized: Optional[bool] = False) -> List[TextMapping]:
    memo = []

    memo.extend(_from_disk(user_mappings))
    memo.extend(_from_disk(default_mappings))

    if remove_unrecognized:
        memo.append(TextMapping(pat=re.compile(r".*"), replacement=""))

    return memo
