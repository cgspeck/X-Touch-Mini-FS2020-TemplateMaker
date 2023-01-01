import argparse
import sys
import time
from pathlib import Path

from template_maker import aircraft_config, gui
from template_maker.config import Config

from template_maker.generator import generate_svgstr, svg_to_png
from template_maker.logger import setup_logger
from template_maker.template_info import TemplateInfo
from template_maker.text_mapping import load_mappings
from template_maker.vars import output_path

logger = setup_logger()
config = Config.load()


def create_parser():
    parser = argparse.ArgumentParser(
        prog="X-Touch Mini FS2020 Template Maker",
        description="Generates svg and png templates from given aircraft configuration",
    )
    parser.add_argument(
        "--config",
        "-c",
        help="Path to aircraft config, if omitted then a file chooser will launch",
    )
    parser.add_argument(
        "--watch",
        "-w",
        action="store_true",
        help="Display generated file an window and reload if aircraft config or string mapping changes",
    )
    parser.add_argument(
        "--preview", "-p", action="store_true", help="Force a preview window to appear"
    )
    return parser


def run_generator(template_info: TemplateInfo):
    svgstr = generate_svgstr(template_info.buttons, template_info.encoders)
    logger.info(f"Writing {template_info.dest_svg}")

    if not output_path.exists():
        output_path.mkdir(parents=True)

    Path(template_info.dest_svg).write_text(svgstr)

    logger.info(f"Writing {template_info.dest_png}")
    svg_to_png(svgstr, template_info.dest_png, config.inkscape_path)


def load_mappings_and_run(logger, config, gui_mode, ac_config):
    mappings = load_mappings(config.remove_unrecognized)
    logger.info(f"Loading '{ac_config}'")
    template_info = parse_ac_config_and_apply_mappings(ac_config, mappings)

    if len(template_info.error_msgs) > 0:
        for m in template_info.error_msgs:
            logger.error(m)

        if gui_mode:
            msg = "\n".join(template_info.error_msgs)
            gui.do_error_box("Error parsing aircraft config", msg)

    fn = f"{int(time.time())}"
    template_info.dest_svg = Path(output_path, f"{fn}.svg")
    template_info.dest_png = Path(output_path, f"{fn}.png")

    run_generator(template_info)
    return template_info


def parse_ac_config_and_apply_mappings(ac_config, mappings):
    template_info = aircraft_config.parse_aircraft_config(ac_config)
    template_info.apply_template_mappings(mappings)
    return template_info


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    gui_mode = False
    ac_config = None

    if args.config is None:
        gui_mode = True
        ac_config = gui.select_aircraft_config(config.xtouch_mini_fs2020_aircraft_path)
        if ac_config is None:
            logger.info("No aircraft config selected")
            sys.exit()

        ac_config = Path(ac_config)
    else:
        ac_config = Path(args.config)

    if args.watch:
        gui_mode = True

    template_info = load_mappings_and_run(logger, config, gui_mode, ac_config)

    if gui_mode or args.preview:
        app = gui.make_preview_app(config, template_info)()
        app.mainloop()
