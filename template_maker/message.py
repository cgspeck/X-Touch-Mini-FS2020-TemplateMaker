from typing import Optional, Union
from uuid import UUID
from dataclasses import dataclass
from enum import auto, Enum
from semver import VersionInfo
from template_maker.template_info import TemplateInfo


class MessageType(Enum):
    GENERATION_COMPLETE = auto()
    MAPPING_UPDATE_CHECK_COMPLETE = auto()
    UPDATE_CHECK_COMPLETE = auto()


@dataclass
class UpdateCheckResult:
    update_available: Optional[bool] = None
    latest_version: Optional[VersionInfo] = None
    latest_url: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class MappingUpdateCheckResult:
    updated: Optional[bool] = None
    latest_version: Optional[VersionInfo] = None
    error_message: Optional[str] = None


@dataclass
class Message:
    job_id: UUID
    message_type: MessageType
    payload: Union[TemplateInfo, MappingUpdateCheckResult, UpdateCheckResult]

    def get_template_info(self) -> TemplateInfo:
        if self.message_type != MessageType.GENERATION_COMPLETE:
            raise ValueError(
                f"Expected message {MessageType.GENERATION_COMPLETE.name}, got {self.message_type.name}"
            )

        if type(self.payload) != TemplateInfo:
            raise ValueError

        return self.payload

    def get_mapping_update_check_result(self) -> MappingUpdateCheckResult:
        if self.message_type != MessageType.MAPPING_UPDATE_CHECK_COMPLETE:
            raise ValueError(
                f"Expected message {MessageType.MAPPING_UPDATE_CHECK_COMPLETE.name}, got {self.message_type.name}"
            )

        if type(self.payload) != MappingUpdateCheckResult:
            raise ValueError

        return self.payload

    def get_update_check_result(self) -> UpdateCheckResult:
        if self.message_type != MessageType.UPDATE_CHECK_COMPLETE:
            raise ValueError(
                f"Expected message {MessageType.UPDATE_CHECK_COMPLETE.name}, got {self.message_type.name}"
            )

        if type(self.payload) != UpdateCheckResult:
            raise ValueError

        return self.payload
