from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from template_maker.button import Button
from template_maker.encoder import Encoder

@dataclass
class TemplateInfo:
    buttons: List[Button]
    encoders: List[Encoder]
    filepath: Path
    error_msgs: List[str]
