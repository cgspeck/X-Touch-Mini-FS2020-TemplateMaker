import re
from typing import List
from template_maker.label import Label

from template_maker.text_mapping import (
    DEFAULT_REPLACEMENT_TEXT,
    TextMapping,
    sanitise_replacement,
)


def generate_mapping_templates(labels: List[Label]) -> List[TextMapping]:
    memo: List[TextMapping] = []
    replacement_unsanitized = sanitise_replacement(DEFAULT_REPLACEMENT_TEXT)

    for l in labels:
        memo.append(
            TextMapping(
                re.compile(l.original),
                DEFAULT_REPLACEMENT_TEXT,
                replacement_unsanitized=replacement_unsanitized,
                in_use=True,
                new=True,
                modified=False,
            )
        )

    return memo
