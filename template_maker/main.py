import argparse
from queue import Queue
import sys
from pathlib import Path
from uuid import uuid4

from template_maker import gui
from template_maker.config import Config
from template_maker.errors import PrerequsitesNotFoundException
from template_maker.generator_thread import GeneratorThread

from template_maker.logger import setup_logger

logger = setup_logger()


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
        "--preview", "-p", action="store_true", help="Force a preview window to appear"
    )
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    gui_mode = False
    ac_config = None

    if args.config is None or args.preview == True:
        gui_mode = True

    try:
        prog_cfg = Config.load()
    except PrerequsitesNotFoundException as err:
        print(err)
        if gui_mode:
            gui.do_error_box("Missing Prerequisites", str(err))
        sys.exit(1)

    if args.config is None:
        ac_config = gui.select_aircraft_config(
            prog_cfg.xtouch_mini_fs2020_aircraft_path
        )
        if ac_config is None:
            logger.info("No aircraft config selected")
            sys.exit()

        ac_config = Path(ac_config)
    else:
        ac_config = Path(args.config)

    job_id = uuid4()
    q = Queue()
    t = GeneratorThread(job_id, q, logger, prog_cfg, ac_config)
    t.start()

    if gui_mode or args.preview:
        app = gui.make_preview_app(prog_cfg, q, job_id)()
        app.mainloop()
    else:
        logger.info("Waiting for generator thread to finish...")
        t.join()
