from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin

from template_maker import vars
from template_maker.label import Label, gather_unmapped_label
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
class EncoderLabels(DataClassJsonMixin):
    primary: Optional[Label] = None
    secondary: Optional[Label] = None
    tertiary: Optional[Label] = None

    def apply_mappings(self, mappings: List[TextMapping], blank_unrecognized: bool):
        if self.primary is not None:
            self.primary.apply_mappings(mappings, blank_unrecognized=blank_unrecognized)

        if self.secondary is not None:
            self.secondary.apply_mappings(
                mappings, blank_unrecognized=blank_unrecognized
            )

        if self.tertiary is not None:
            self.tertiary.apply_mappings(
                mappings, blank_unrecognized=blank_unrecognized
            )

    def gather_unmapped_labels(self) -> List[Label]:
        memo = []
        memo.extend(gather_unmapped_label(self, "primary"))
        memo.extend(gather_unmapped_label(self, "secondary"))
        memo.extend(gather_unmapped_label(self, "tertiary"))
        return memo


@dataclass
class Encoder(DataClassJsonMixin):
    index: int
    layer_a: Optional[EncoderLabels] = None
    layer_b: Optional[EncoderLabels] = None

    def __post_init__(self):
        if self.index < 1 or self.index > 8:
            raise ValueError(f"Expected index in range 1 - 8, got {self.index}")

        self.mid_x = encoder_x_origin + encoder_rad + (self.index - 1) * encoder_x_dist

    def apply_mappings(
        self, mappings: List[TextMapping], blank_unrecognized: bool
    ) -> None:
        if self.layer_a is not None:
            self.layer_a.apply_mappings(mappings, blank_unrecognized)

        if self.layer_b is not None:
            self.layer_b.apply_mappings(mappings, blank_unrecognized)

    def emit_mask(self) -> str:
        return f'<circle cx="{self.mid_x}" cy="{encoder_y_origin + encoder_rad}" r="{encoder_rad}" fill="black" />\n'

    def _emit_secondary_tertiary_text(self) -> str:
        secondary = None
        tertiary = None
        memo = ""

        layer_a = self.layer_a

        if layer_a is None:
            return memo

        if layer_a.secondary is not None and layer_a.secondary.display_text_has_content:
            secondary = layer_a.secondary.display

        if layer_a.tertiary is not None and layer_a.tertiary.display_text_has_content:
            tertiary = layer_a.tertiary.display

        if secondary is not None and tertiary is not None:
            memo = f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{secondary} ({tertiary})</text>\n'
        elif secondary is not None:
            memo = f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{secondary}</text>\n'
        elif tertiary is not None:
            memo = f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_secondary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{tertiary}</text>\n'

        return memo

    def emit_text(self) -> str:
        memo = ""
        layer_a = self.layer_a

        if (
            layer_a is not None
            and layer_a.primary is not None
            and layer_a.primary.display_text_has_content
        ):
            memo += f'<text x="{self.mid_x}" y="{encoder_y_primary_text}" font-size="{encoder_primary_font_size}" text-anchor="middle" fill="white" font-family="{vars.font_family}">{layer_a.primary.display}</text>\n'

        memo += self._emit_secondary_tertiary_text()

        return memo

    def gather_unmapped_labels(self) -> List[Label]:
        memo = []
        if self.layer_a is not None:
            memo.extend(self.layer_a.gather_unmapped_labels())

        if self.layer_b is not None:
            memo.extend(self.layer_b.gather_unmapped_labels())
        return memo
