from dataclasses import dataclass
from typing import Any, List, Optional

from dataclasses_json import DataClassJsonMixin

from template_maker.text_mapping import TextMapping


@dataclass
class Label(DataClassJsonMixin):
    original: Optional[str] = None
    display: Optional[str] = None
    replaced: bool = False

    def __lt__(self, other: Any):
        if type(other) == Label:
            return self.original < other.original

        if type(other) != Label:
            raise ValueError(f"Unable to compare Label against {type(other)}")

    @property
    def display_text_has_content(self) -> bool:
        return self.display is not None and len(self.display.strip()) > 0

    def apply_mappings(
        self, mappings: List[TextMapping], blank_unrecognized: bool
    ) -> None:
        if self.original is None:
            return

        self.display = self.original
        self.replaced = False

        for m in mappings:
            if m.pat.search(self.original):
                self.display = m.replacement
                self.replaced = True
                m.in_use = True
                break

        if blank_unrecognized and not self.replaced:
            self.display = ""


def gather_unmapped_label(obj, property) -> List[Label]:
    label_obj = getattr(obj, property)

    if label_obj is None:
        return []

    if not label_obj.display is None and not label_obj.replaced:
        return [label_obj]

    return []
