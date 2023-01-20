import html
import re
from dataclasses import dataclass
from pathlib import Path
from re import Pattern
from typing import Any, List

from dataclasses_json import DataClassJsonMixin

from template_maker.logger import get_logger
from template_maker.vars import default_mappings, user_mappings

DEFAULT_REPLACEMENT_TEXT = "SET ME!"

logger = get_logger()


@dataclass
class TextMapping(DataClassJsonMixin):
    pat: Pattern
    replacement: str
    replacement_unsanitized: str
    in_use: bool = False
    new: bool = False
    modified: bool = False

    def __lt__(self, other: Any):
        if type(other) == TextMapping:
            return str(self.pat) < str(other.pat)

        if type(other) != TextMapping:
            raise ValueError(f"Unable to compare TextMapping against {type(other)}")


def sanitise_replacement(original: str) -> str:
    return html.escape(original)


def parse_file(fp: Path) -> List[TextMapping]:
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
        memo.append(
            TextMapping(
                pat=re.compile(k),
                replacement=sanitise_replacement(v),
                replacement_unsanitized=v,
                in_use=False,
            )
        )
    return memo


def load_mappings() -> List[TextMapping]:
    memo = []

    memo.extend(parse_file(user_mappings))

    if len(memo) == 0:
        reset_mappings()
        return load_mappings()

    return memo


def save_mappings(mappings: List[TextMapping]):
    with user_mappings.open("wt") as fh:
        for m in mappings:
            fh.write(f"{m.pat.pattern} = {m.replacement_unsanitized}\n")


def reset_mappings():
    logger.info(f"Resetting mappings: {user_mappings}")
    user_mappings.write_text(default_mappings.read_text())
