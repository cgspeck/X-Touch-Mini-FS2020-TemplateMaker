
from dataclasses import dataclass
from typing import List, Optional

from template_maker import vars
from template_maker.text_mapping import TextMapping

# reference height is mm
encoder_x_origin = 4
encoder_x_dist = 31.2
encoder_y_origin = 10.7
encoder_dia = 25
encoder_rad = encoder_dia/2
encoder_y_primary_text = 9
encoder_y_secondary_text = encoder_y_origin + encoder_dia + 6
encoder_primary_font_size = 7
encoder_secondary_font_size = 5


@dataclass
class Encoder:
    index: int
    layer_a_primary_text: Optional[str] = None
    layer_a_secondary_text: Optional[str] = None
    layer_a_tertiary_text: Optional[str] = None

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

        if self.layer_a_tertiary_text is not None:
            for m in mappings:
                if m.pat.search(self.layer_a_tertiary_text):
                    self.layer_a_tertiary_text = m.replacement
                    break

    def emit_mask(self) -> str:
        return f'<circle cx="{self.mid_x}" cy="{encoder_y_origin + encoder_rad}" r="{encoder_rad}" fill="black" />\n'

    def emit_text(self) -> str:
        memo = ""

        if self.layer_a_primary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_primary_text}" font-size="{encoder_primary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_primary_text}</text>'

        if self.layer_a_secondary_text is not None and self.layer_a_tertiary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_secondary_text} ({self.layer_a_tertiary_text})</text>'
        elif self.layer_a_secondary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_secondary_text}</text>'
        elif self.layer_a_tertiary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_tertiary_text}</text>'

        return memo
