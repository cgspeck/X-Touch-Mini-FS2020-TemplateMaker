from dataclasses import dataclass
from typing import Optional


@dataclass(eq=True, order=True)
class EventPressDefinition:
    event: Optional[str]
    value: Optional[str]
