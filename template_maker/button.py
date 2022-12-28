
from dataclasses import dataclass
from typing import List, Optional

from template_maker import vars
from template_maker.text_mapping import TextMapping

button_dim = [47.2, 35.4]
button_x_origin = 69.85
button_x_dist = 122.5
button_y_origin = 186
button_y_dist = 87
button_font_size = 16


@dataclass
class Button:
    index: int
    layer_a_text: Optional[str] = None

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

        self.text_y = self.y + button_dim[1] + 18

    def apply_mappings(self, mappings: List[TextMapping]) -> None:
        for m in mappings:
            if m.pat.search(self.layer_a_text):
                self.layer_a_text = m.replacement
                break

    def emit_mask(self) -> str:
        return f'<rect x="{self.x}" y="{self.y}" width="{button_dim[0]}" height="{button_dim[1]}" fill="black" />\n'

    def emit_text(self) -> str:
        memo = ""

        if self.layer_a_text is not None:
            memo += f'<text x="{self.mid_x}" y="{self.text_y}" font-size="{button_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_text}</text>'

        return memo

