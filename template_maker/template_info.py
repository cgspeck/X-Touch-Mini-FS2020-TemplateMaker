from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, config
from template_maker.button import Button
from template_maker.encoder import Encoder
from template_maker.text_mapping import TextMapping


@dataclass
class TemplateInfo(DataClassJsonMixin):
    buttons: List[Button]
    encoders: List[Encoder]
    filepath: Path = field(metadata=config(encoder=str, decoder=Path))
    error_msgs: List[str] = field(default_factory=list)
    dest_svg: Optional[Path] = None
    dest_png: Optional[Path] = None

    def apply_template_mappings(self, mappings: List[TextMapping]) -> None:
        for button in self.buttons:
            button.apply_mappings(mappings)

        for encoder in self.encoders:
            encoder.apply_mappings(mappings)
