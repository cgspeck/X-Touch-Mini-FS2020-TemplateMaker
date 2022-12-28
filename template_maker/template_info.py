from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from re import Pattern
from template_maker.button import Button
from template_maker.encoder import Encoder
from template_maker.text_mapping import TextMapping

@dataclass
class TemplateInfo:
    buttons: List[Button]
    encoders: List[Encoder]
    filepath: Path
    error_msgs: List[str]

    def apply_template_mappings(self, mappings: List[TextMapping]) -> None:
        for button in self.buttons:
            button.apply_mappings(mappings)

        for encoder in self.encoders:
            encoder.apply_mappings(mappings)

