from logging import Logger
from queue import Queue
from threading import Thread
from typing import Any, Optional
from uuid import UUID

import yaml


from template_maker.message import (
    MappingUpdateCheckResult,
    Message,
    MessageType,
)
from template_maker import vars

from typing import Optional
from queue import Queue
import urllib.request

from semver import VersionInfo

from template_maker.text_mapping import get_default_mapping_version


LATEST_MAPPING_FILE = "https://raw.githubusercontent.com/cgspeck/X-Touch-Mini-FS2020-TemplateMaker-Mappings/main/mappings.default.yaml"
MAX_MAJOR_VERSION = 2


class MappingUpdateCheckThread(Thread):
    def __init__(
        self,
        job_id: UUID,
        queue: Queue,
        logger: Logger,
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

    def run(self):
        try:
            fh = urllib.request.urlopen(LATEST_MAPPING_FILE)
            dct = yaml.load(fh.read(), Loader=yaml.Loader)
            latest_version: VersionInfo = dct["version"]
            current_mapping_version = get_default_mapping_version()

            if latest_version.major > MAX_MAJOR_VERSION:
                memo = MappingUpdateCheckResult(
                    error_message=f"Mapping version {latest_version} is available but this application\nonly supports mappings versions 1.x.y.\n\nPlease check for application updates."
                )
            elif latest_version > current_mapping_version:
                vars.default_mappings.write_text(yaml.dump(dct))
                memo = MappingUpdateCheckResult(
                    updated=True, latest_version=latest_version
                )
            else:
                memo = MappingUpdateCheckResult(
                    updated=False, latest_version=latest_version
                )

        except Exception as err:
            memo = MappingUpdateCheckResult(
                error_message=f"Unable to check for updates:\n{err}"
            )

        self.queue.put(
            Message(
                job_id=self.job_id,
                message_type=MessageType.MAPPING_UPDATE_CHECK_COMPLETE,
                payload=memo,
            )
        )
