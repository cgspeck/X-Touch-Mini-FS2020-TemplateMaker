from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, config
from template_maker.button import Button
from template_maker.encoder import Encoder
from template_maker.label import Label
from template_maker.text_mapping import TextMapping


@dataclass
class TemplateInfo(DataClassJsonMixin):
    buttons: List[Button]
    encoders: List[Encoder]
    filepath: Path = field(metadata=config(encoder=str, decoder=Path))
    error_msgs: List[str] = field(default_factory=list)
    dest_svg: Optional[Path] = None
    dest_png: Optional[Path] = None
    mappings: List[TextMapping] = field(default_factory=list)

    _unmapped_labels: Optional[List[Label]] = None

    def apply_template_mappings(
        self, blank_unrecognized: bool, defaults_enabled: bool
    ) -> None:
        for button in self.buttons:
            button.apply_mappings(self.mappings, blank_unrecognized, defaults_enabled)

        for encoder in self.encoders:
            encoder.apply_mappings(self.mappings, blank_unrecognized, defaults_enabled)

    def gather_unmapped_labels(self) -> List[Label]:
        if self._unmapped_labels is not None:
            return self._unmapped_labels

        memo: List[Label] = []

        for button in self.buttons:
            memo.extend(button.gather_unmapped_labels())

        for encoder in self.encoders:
            memo.extend(encoder.gather_unmapped_labels())

        memo.sort()
        uniq = []

        for i in memo:
            if i not in uniq:
                uniq.append(i)

        self._unmapped_labels = uniq
        return self.gather_unmapped_labels()
