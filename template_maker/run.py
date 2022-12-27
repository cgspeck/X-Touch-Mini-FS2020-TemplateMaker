from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

fn = "test"
dest_svg = Path("out", f"{fn}.svg")
dest_png = Path("out", f"{fn}.png")

base_dim = [1024, 370]

button_dim = [47.2, 35.4]
button_x_origin = 69.85
button_x_dist = 122.5
button_y_origin = 186
button_y_dist = 87
button_font_size = 16

encoder_x_origin = 45
encoder_x_dist = 122.5
encoder_y_origin = 45
encoder_y_primary_text = 30
encoder_y_secondary_text = 170
encoder_rad = 47.2
encoder_font_size = 26

font_family = "monospace"


@dataclass
class Button:
    index: int
    text: Optional[str] = None

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

    def emit_mask(self) -> str:
        return f'<rect x="{self.x}" y="{self.y}" width="{button_dim[0]}" height="{button_dim[1]}" fill="black" />\n'

    def emit_text(self) -> str:
        memo = ""

        if self.text is not None:
            memo += f'<text x="{self.mid_x}" y="{self.text_y}" font-size="{button_font_size}" text-anchor="middle" fill="white" font-family="{font_family}">{self.text}</text>'

        return memo


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
            memo += f'<text x="{self.mid_x}" y="{encoder_y_primary_text}" font-size="{encoder_font_size}" text-anchor="middle" fill="white" font-family="{font_family}">{self.primary_text}</text>'

        if self.secondary_text is not None:
            memo += f'<text x="{self.mid_x}" y="{encoder_y_secondary_text}" font-size="{encoder_font_size}" text-anchor="middle" fill="white" font-family="{font_family}">{self.secondary_text}</text>'

        return memo


encoders = [
    Encoder(1, "1", "1SecFN"),
    Encoder(2, "2", "2SecFN"),
    Encoder(3, "3"),
    Encoder(4, "4"),
    Encoder(5, "5"),
    Encoder(6, "6"),
    Encoder(7, "7"),
    Encoder(8, "8"),
]

buttons = [
    Button(1, "1"),
    Button(2, "2"),
    Button(3, "3"),
    Button(4, "4"),
    Button(5, "5"),
    Button(6, "6"),
    Button(7, "7"),
    Button(8, "8"),
    Button(9, "9"),
    Button(10, "10"),
    Button(11, "11"),
    Button(12, "12"),
    Button(13, "13"),
    Button(14, "14"),
    Button(15, "15"),
    Button(16, "16"),
]

memo = f'<svg version="1.1" width="{base_dim[0]}" height="{base_dim[1]}" xmlns="http://www.w3.org/2000/svg">\n'
memo += "<defs>"
memo += '<mask id="encoder_holes">\n'
memo += '<rect width="100%" height="100%" rx="15" fill="white" />\n'
for encoder in encoders:
    memo += encoder.emit_mask()

for button in buttons:
    memo += button.emit_mask()

memo += "</mask>\n"
memo += "</defs>"

memo += "<g>\n"
memo += '<rect width="100%" height="100%" rx="15" fill="dimgray" mask="url(#encoder_holes)" />\n'
for encoder in encoders:
    memo += encoder.emit_text()

for button in buttons:
    memo += button.emit_text()

memo += "</g>\n"
memo += "</svg>"

print(f"Writing {dest_svg}")
Path(dest_svg).write_text(memo)

#
# FIXME: the png is missing the transparent cutouts
#        see if there are any switches or change to Inkscape?
#
# "C:\Program Files\Inkscape\bin\inkscape.exe" --export-filename "foo.png" test.svg
print(f"Writing {dest_png}")
drawing = svg2rlg(dest_svg, resolve_entities=True)
renderPM.drawToFile(drawing, dest_png, fmt="PNG")
