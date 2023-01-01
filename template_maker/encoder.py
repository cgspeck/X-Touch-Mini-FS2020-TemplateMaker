from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin

from template_maker import vars
from template_maker.label import Label
from template_maker.text_mapping import TextMapping

# reference height is mm
encoder_x_origin = 4
encoder_x_dist = 31.2
encoder_y_origin = 10.7
encoder_dia = 25
encoder_rad = encoder_dia / 2
encoder_y_primary_text = 9
encoder_y_secondary_text = encoder_y_origin + encoder_dia + 6
encoder_primary_font_size = 7
encoder_secondary_font_size = 5


@dataclass
class Encoder(DataClassJsonMixin):
    index: int
    layer_a_primary_text: Optional[Label] = None
    layer_a_secondary_text: Optional[Label] = None
    layer_a_tertiary_text: Optional[Label] = None

    def __post_init__(self):
        if self.index < 1 or self.index > 8:
            raise ValueError(f"Expected index in range 1 - 8, got {self.index}")

        self.mid_x = encoder_x_origin + encoder_rad + (self.index - 1) * encoder_x_dist

    def apply_mappings(self, mappings: List[TextMapping]) -> None:
        if self.layer_a_primary_text is not None:
            self.layer_a_primary_text.apply_mappings(mappings)

        if self.layer_a_secondary_text is not None:
            self.layer_a_secondary_text.apply_mappings(mappings)

        if self.layer_a_tertiary_text is not None:
            self.layer_a_tertiary_text.apply_mappings(mappings)

    def emit_mask(self) -> str:
        return f'<circle cx="{self.mid_x}" cy="{encoder_y_origin + encoder_rad}" r="{encoder_rad}" fill="black" />\n'

    def _emit_secondary_tertiary_text(self) -> str:
        secondary_text = None
        tertiary_text = None
        memo = ""

        if self.layer_a_secondary_text is not None:
            secondary_text = self.layer_a_secondary_text.display

        if self.layer_a_tertiary_text is not None:
            tertiary_text = self.layer_a_tertiary_text.display

        if secondary_text is not None and tertiary_text is not None:
            memo = f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{secondary_text} ({tertiary_text})</text>\n'
        elif secondary_text is not None:
            memo = f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{secondary_text}</text>\n'
        elif tertiary_text is not None:
            memo = f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{tertiary_text}</text>\n'

        return memo

    def emit_text(self) -> str:
        memo = ""

        if self.layer_a_primary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_primary_text}" font-size="{encoder_primary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.layer_a_primary_text.display or ""}</text>\n'

        memo += self._emit_secondary_tertiary_text()

        return memo
