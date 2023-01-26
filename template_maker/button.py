from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin

from template_maker import vars
from template_maker.label import Label, gather_unmapped_label
from template_maker.text_mapping import TextMapping

# in mm
button_dim = [13, 10]
button_x_origin = 9.5
button_x_dist = 31.2
button_y_origin = 47.6
button_y_dist = 20.2
label_y_gap = 5
button_font_size = 5


@dataclass
class ButtonLabels(DataClassJsonMixin):
    primary: Optional[Label] = None
    secondary: Optional[Label] = None

    def apply_mappings(
        self,
        mappings: List[TextMapping],
        blank_unrecognized: bool,
        defaults_enabled: bool,
    ):
        if self.primary is not None:
            self.primary.apply_mappings(
                mappings,
                blank_unrecognized=blank_unrecognized,
                defaults_enabled=defaults_enabled,
            )

        if self.secondary is not None:
            self.secondary.apply_mappings(
                mappings,
                blank_unrecognized=blank_unrecognized,
                defaults_enabled=defaults_enabled,
            )

    def gather_unmapped_labels(self) -> List[Label]:
        memo = []
        memo.extend(gather_unmapped_label(self, "primary"))
        memo.extend(gather_unmapped_label(self, "secondary"))
        return memo


@dataclass
class Button(DataClassJsonMixin):
    index: int
    layer_a: Optional[ButtonLabels] = None
    layer_b: Optional[ButtonLabels] = None

    def __post_init__(self):
        if self.index < 1 or self.index > 16:
            raise ValueError(f"Expected index in range 1 - 16, got {self.index}")

        _index = self.index

        if _index > 8:
            _index = _index - 8

        self.x = button_x_origin + (_index - 1) * button_x_dist
        self.mid_x = self.x + button_dim[0] / 2
        self.y = button_y_origin

        if self.index > 8:
            self.y = self.y + button_y_dist

        self.text_y = self.y + button_dim[1] + label_y_gap

    def apply_mappings(
        self,
        mappings: List[TextMapping],
        blank_unrecognized: bool,
        defaults_enabled: bool,
    ) -> None:
        if self.layer_a is not None:
            self.layer_a.apply_mappings(mappings, blank_unrecognized, defaults_enabled)

        if self.layer_b is not None:
            self.layer_b.apply_mappings(mappings, blank_unrecognized, defaults_enabled)

    def emit_mask(self) -> str:
        return f'<rect x="{self.x}" y="{self.y}" width="{button_dim[0]}" height="{button_dim[1]}" fill="black" />\n'

    def emit_text(self) -> str:
        memo = ""

        if self.layer_a is not None and self.layer_a.primary is not None:
            memo += f'<text x="{self.mid_x}" y="{self.text_y}" font-size="{button_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a.primary.display or ""}</text>\n'

        return memo

    def gather_unmapped_labels(self) -> List[Label]:
        memo = []
        if self.layer_a is not None:
            memo.extend(self.layer_a.gather_unmapped_labels())

        if self.layer_b is not None:
            memo.extend(self.layer_b.gather_unmapped_labels())
        return memo
