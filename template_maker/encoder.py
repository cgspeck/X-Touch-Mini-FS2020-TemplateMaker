
from dataclasses import dataclass
from typing import Optional

from template_maker import vars

encoder_x_origin = 45
encoder_x_dist = 122.5
encoder_y_origin = 45
encoder_y_primary_text = 30
encoder_y_secondary_text = 170
encoder_rad = 47.2
encoder_font_size = 26


@dataclass
class Encoder:
    index: int
    primary_text: Optional[str] = None
    secondary_text: Optional[str] = None

    def __post_init__(self):
        if self.index < 1 or self.index > 8:
            raise ValueError(f"Expected index in range 1 - 8, got {self.index}")

        self.mid_x = encoder_x_origin + encoder_rad + (self.index - 1) * encoder_x_dist

    def emit_mask(self) -> str:
        return f'<circle cx="{self.mid_x}" cy="{encoder_y_origin + encoder_rad}" r="{encoder_rad}" fill="black" />\n'

    def emit_text(self) -> str:
        memo = ""

        if self.primary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_primary_text}" font-size="{encoder_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.primary_text}</text>'

        if self.secondary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{self.secondary_text}</text>'

        return memo
