from logging import Logger
from queue import Queue
from threading import Thread
from typing import Any, Optional
from uuid import UUID


from template_maker.message import Message, MessageType, UpdateCheckResult

from typing import Optional
from queue import Queue
import urllib.request
import json

from semver import VersionInfo


UPDATE_CHECK_ENDPOINT = "https://api.github.com/repos/cgspeck/X-Touch-Mini-FS2020-TemplateMaker/releases/latest"


class UpdateCheckThread(Thread):
    def __init__(
        self,
        job_id: UUID,
        queue: Queue,
        logger: Logger,
        my_version: VersionInfo,
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
        self.my_version = my_version

    def run(self):
        try:
            fh = urllib.request.urlopen(UPDATE_CHECK_ENDPOINT)
            dct = json.load(fh)
            latest_version_str: str = dct["name"].strip("v")
            latest_version = VersionInfo.parse(latest_version_str)
            memo = UpdateCheckResult(
                update_available=latest_version > self.my_version,
                latest_version=latest_version,
                latest_url=dct["html_url"],
            )
        except Exception as err:
            memo = UpdateCheckResult(
                error_message=f"Unable to check for updates:\n{err}"
            )

        self.queue.put(
            Message(
                job_id=self.job_id,
                message_type=MessageType.UPDATE_CHECK_COMPLETE,
                payload=memo,
            )
        )
