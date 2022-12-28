import argparse
import sys
import time
from pathlib import Path
from typing import List

from template_maker import aircraft_config, gui
from template_maker.button import Button
from template_maker.config import Config

from template_maker.encoder import Encoder
from template_maker.generator import generate_svgstr, svg_to_png
from template_maker.logger import setup_logger
from template_maker.template_info import TemplateInfo
from template_maker.text_mapping import TextMapping
from template_maker.vars import output_path

logger = setup_logger()
config = Config.load()


def create_parser():
    parser = argparse.ArgumentParser(
        prog="X-Touch Mini FS2020 Template Maker",
        description="Generates svg and png templates from given aircraft configuration",
    )
    parser.add_argument('--config', '-c', help="Path to aircraft config, if omitted then a file chooser will launch")
    parser.add_argument('--watch', "-w", action='store_true', help="Display generated file an window and reload if aircraft config or string mapping changes")    
    return parser

def run(template_info: TemplateInfo, dest_svg: Path, dest_png: Path):
    svgstr = generate_svgstr(template_info.buttons, template_info.encoders)
    logger.info(f"Writing {dest_svg}")

    if not output_path.exists():
        output_path.mkdir()

    Path(dest_svg).write_text(svgstr)

    logger.info(f"Writing {dest_png}")
    svg_to_png(svgstr, dest_png, config.inkscape_path)

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    gui_mode = False

    if args.config is None:
        gui_mode = True
        ac_config = gui.select_aircraft_config(config.xtouch_mini_fs2020_aircraft_path)
        if ac_config is None:
            logger.info('No aircraft config selected')
            sys.exit()
        
        ac_config = Path(ac_config)
    else:
        ac_config = Path(args.config)

    if args.watch:
        gui_mode = True

    template_info = aircraft_config.parse_aircraft_config(ac_config)

    template_info.apply_template_mappings([])

    if len(template_info.error_msgs) > 0:
        for m in template_info.error_msgs:
            logger.error(m)

        if gui_mode:
            msg = "\n".join(template_info.error_msgs)
            gui.do_error_box("Error parsing aircraft config", msg)

    fn = f"{int(time.time())}"
    dest_svg = Path(output_path, f"{fn}.svg")
    dest_png = Path(output_path, f"{fn}.png")

    run(template_info, dest_svg, dest_png)

    if gui_mode:
        app = gui.make_preview_app(dest_png)()
        app.mainloop()
