from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin

from template_maker import vars
from template_maker.label import Label
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
class Button(DataClassJsonMixin):
    index: int
    layer_a_text: Optional[Label] = None

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

    def apply_mappings(self, mappings: List[TextMapping]) -> None:
        if self.layer_a_text is None:
            return

        self.layer_a_text.apply_mappings(mappings)

    def emit_mask(self) -> str:
        return f'<rect x="{self.x}" y="{self.y}" width="{button_dim[0]}" height="{button_dim[1]}" fill="black" />\n'

    def emit_text(self) -> str:
        memo = ""

        if self.layer_a_text is not None:
            memo += f'<text x="{self.mid_x}" y="{self.text_y}" font-size="{button_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_text.display or ""}</text>\n'

        return memo
