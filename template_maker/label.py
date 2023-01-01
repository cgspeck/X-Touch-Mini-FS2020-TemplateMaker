from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin

from template_maker.text_mapping import TextMapping


@dataclass
class Label(DataClassJsonMixin):
    original: Optional[str] = None
    display: Optional[str] = None
    replaced: bool = False

    def apply_mappings(self, mappings: List[TextMapping]) -> None:
        if self.original is None:
            return

        self.display = self.original
        self.replaced = False

        for m in mappings:
            if m.pat.search(self.original):
                self.display = m.replacement
                self.replaced = True
                break
