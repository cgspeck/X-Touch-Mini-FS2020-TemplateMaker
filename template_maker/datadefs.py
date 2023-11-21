from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin


@dataclass(eq=True, order=True)
class EventPressDefinition(DataClassJsonMixin):
    event: Optional[str]
    value: Optional[str]
