import argparse
from queue import Queue
import sys
from pathlib import Path
from uuid import uuid4

from template_maker import gui
from template_maker.config import Config
from template_maker.generator_thread import GeneratorThread

from template_maker.logger import setup_logger

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
        "--preview", "-p", action="store_true", help="Force a preview window to appear"
    )
    return parser


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

    job_id = uuid4()
    q = Queue()
    t = GeneratorThread(job_id, q, logger, config, ac_config)
    t.start()

    if gui_mode or args.preview:
        app = gui.make_preview_app(config, q, job_id)()
        app.mainloop()
    else:
        logger.info("Waiting for generator thread to finish...")
        t.join()
