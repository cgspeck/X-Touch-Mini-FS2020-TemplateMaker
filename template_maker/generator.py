import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

from template_maker.button import Button
from template_maker.encoder import Encoder
from template_maker.logger import get_logger

logger = get_logger()

base_dim = [1024, 370]

def generate_svgstr(buttons: List[Button], encoders: List[Encoder]) -> str:
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
    return memo

def svg_to_png(svgstr: str, filename: Path, inkscape_path: Path) -> None:
    tf = tempfile.NamedTemporaryFile("wt", suffix=".svg", delete=False)
    tf.write(svgstr)
    tf.close()
    args = [
        str(inkscape_path),
        '--export-filename',
        f'{filename}',
        f'{tf.name}'
    ]
    err = None

    try:
        logger.info(f"Running: {args}")
        subprocess.run(args, check=True)
    except Exception as e:
        err = e
    finally:
        os.unlink(tf.name)

    if e is not None:
        raise e
