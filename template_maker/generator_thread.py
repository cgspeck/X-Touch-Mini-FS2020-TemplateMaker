from logging import Logger
from queue import Queue
from threading import Thread
import time
from pathlib import Path
from typing import Any, List, Optional
from uuid import UUID

from template_maker import aircraft_config
from template_maker.config import Config

from template_maker.generator_util import generate_svgstr, svg_to_png
from template_maker.message import Message, MessageType
from template_maker.template_info import TemplateInfo
from template_maker.text_mapping import TextMapping, load_mappings
from template_maker.vars import output_path


class GeneratorThread(Thread):
    def __init__(
        self,
        job_id: UUID,
        queue: Queue,
        logger: Logger,
        config: Config,
        ac_config: Path,
        group: None = None,
        name: Optional[str] = None,
        daemon: Optional[Any] = None,
    ) -> None:
        super().__init__(
            group=group, target=None, name=name, args=(), kwargs=None, daemon=daemon
        )
        self.job_id = job_id
        self.queue = queue
        self.logger = logger
        self.config = config
        self.ac_config = ac_config

    def run(self):
        self.logger.info(f"Generation job started: {self.job_id}")
        res = self.load_mappings_and_run()
        self.queue.put(
            Message(
                job_id=self.job_id,
                message_type=MessageType.GENERATION_COMPLETE,
                payload=res,
            )
        )

    def load_mappings_and_run(self) -> TemplateInfo:
        mappings = load_mappings()
        self.logger.info(f"Loading '{self.ac_config}'")
        template_info: TemplateInfo = self.parse_ac_config_and_apply_mappings(
            mappings, self.config.remove_unrecognized
        )

        if len(template_info.error_msgs) > 0:
            for m in template_info.error_msgs:
                self.logger.error(m)

        fn = f"{int(time.time())}"
        template_info.dest_svg = Path(output_path, f"{fn}.svg")
        template_info.dest_png = Path(output_path, f"{fn}.png")

        self.run_generator(template_info)
        return template_info

    def run_generator(self, template_info: TemplateInfo) -> None:
        svgstr = generate_svgstr(template_info.buttons, template_info.encoders)
        self.logger.info(f"Writing {template_info.dest_svg}")

        if not output_path.exists():
            output_path.mkdir(parents=True)

        if template_info.dest_svg is None:
            raise ValueError

        Path(template_info.dest_svg).write_text(svgstr)

        if template_info.dest_png is None:
            raise ValueError

        self.logger.info(f"Writing {template_info.dest_png}")
        svg_to_png(svgstr, template_info.dest_png, self.config.inkscape_path)

    def parse_ac_config_and_apply_mappings(
        self, mappings: List[TextMapping], blank_unrecognized: bool
    ) -> TemplateInfo:
        template_info = aircraft_config.parse_aircraft_config(self.ac_config)
        template_info.mappings = mappings
        template_info.apply_template_mappings(blank_unrecognized)
        return template_info
