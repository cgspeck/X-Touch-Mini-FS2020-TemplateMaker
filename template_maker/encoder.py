
from dataclasses import dataclass
from typing import List, Optional

from template_maker import vars
from template_maker.text_mapping import TextMapping

encoder_x_origin = 45
encoder_x_dist = 122.5
encoder_y_origin = 45
encoder_y_primary_text = 30
encoder_y_secondary_text = 170
encoder_rad = 47.2
encoder_primary_font_size = 26
encoder_secondary_font_size = 16


@dataclass
class Encoder:
    index: int
    layer_a_primary_text: Optional[str] = None
    layer_a_secondary_text: Optional[str] = None

    def __post_init__(self):
        if self.index < 1 or self.index > 8:
            raise ValueError(f"Expected index in range 1 - 8, got {self.index}")

        self.mid_x = encoder_x_origin + encoder_rad + (self.index - 1) * encoder_x_dist

    def apply_mappings(self, mappings: List[TextMapping]) -> None:
        if self.layer_a_primary_text is not None:
            print(self.layer_a_primary_text)
            for m in mappings:
                if m.pat.search(self.layer_a_primary_text):
                    self.layer_a_primary_text = m.replacement
                    break

        if self.layer_a_secondary_text is not None:
            for m in mappings:
                if m.pat.search(self.layer_a_secondary_text):
                    self.layer_a_secondary_text = m.replacement
                    break

    def emit_mask(self) -> str:
        return f'<circle cx="{self.mid_x}" cy="{encoder_y_origin + encoder_rad}" r="{encoder_rad}" fill="black" />\n'

    def emit_text(self) -> str:
        memo = ""

        if self.layer_a_primary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_primary_text}" font-size="{encoder_primary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_primary_text}</text>'

        if self.layer_a_secondary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_secondary_text}</text>'

        return memo
