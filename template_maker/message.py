from uuid import UUID
from dataclasses import dataclass
from enum import auto, Enum

from template_maker.template_info import TemplateInfo


class MessageType(Enum):
    GENERATION_COMPLETE = auto()


@dataclass
class Message:
    job_id: UUID
    message_type: MessageType
    payload: TemplateInfo

    def get_template_info(self) -> TemplateInfo:
        if self.message_type != MessageType.GENERATION_COMPLETE:
            raise ValueError(
                f"Expected message {MessageType.GENERATION_COMPLETE.name}, got {self.message_type.name}"
            )

        return self.payload
