from pathlib import Path
from template_maker.button import Button
from template_maker.config import Config
from template_maker.encoder import Encoder
from template_maker.generator import generate_svgstr, svg_to_png
from template_maker.logger import setup_logger

logger = setup_logger()
config = Config.load()


fn = "test"
dest_svg = Path("out", f"{fn}.svg")
dest_png = Path(Path.cwd(), "out", f"{fn}.png")

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

svgstr = generate_svgstr(buttons, encoders)
logger.info(f"Writing {dest_svg}")
Path(dest_svg).write_text(svgstr)

logger.info(f"Writing {dest_png}")
svg_to_png(svgstr, dest_png, config.inkscape_path)
