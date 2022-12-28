
from dataclasses import dataclass
from re import Pattern


@dataclass
class TextMapping:
    pat: Pattern
    replacement: str
