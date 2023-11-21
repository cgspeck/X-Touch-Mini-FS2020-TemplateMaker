from dataclasses import dataclass
from typing import Any, List, Optional

from dataclasses_json import DataClassJsonMixin
from template_maker.datadefs import EventPressDefinition

from template_maker.text_mapping import TextMapping


@dataclass
class Label(DataClassJsonMixin):
    original: Optional[EventPressDefinition] = None
    display: Optional[str] = None
    replaced: bool = False

    def __lt__(self, other: Any):
        if type(other) == Label:
            if self.original is None and other.original:
                return False

            if self.original is None:
                return True

            if other.original is None:
                return False

            return self.original < other.original

        if type(other) != Label:
            raise ValueError(f"Unable to compare Label against {type(other)}")

    @property
    def display_text_has_content(self) -> bool:
        return self.display is not None and len(self.display.strip()) > 0

    def apply_mappings(
        self,
        mappings: List[TextMapping],
        blank_unrecognized: bool,
        defaults_enabled: bool,
    ) -> None:
        if self.original is None:
            return

        event = self.original.event

        if event is None:
            return

        self.display = event
        self.replaced = False
        value = self.original.value

        for m in mappings:
            if m.is_default and not defaults_enabled:
                continue

            match value is None:
                case True:
                    if m.pat.search(event):
                        self.display = m.replacement
                        self.replaced = True
                        m.in_use = True
                        break

                case False:
                    if m.value_pat is None:
                        continue

                    if m.pat.search(event) and m.value_pat.search(value):
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
