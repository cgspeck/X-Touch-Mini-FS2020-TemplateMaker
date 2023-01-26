import html
import re
from dataclasses import dataclass
from pathlib import Path
from re import Pattern
from typing import Any, List, Union

import yaml
from dataclasses_json import DataClassJsonMixin
from semver import VersionInfo
from yaml import FullLoader, Loader, UnsafeLoader

from template_maker import vars
from template_maker.logger import get_logger

DEFAULT_REPLACEMENT_TEXT = "SET ME!"

logger = get_logger()


@dataclass
class TextMapping(DataClassJsonMixin):
    pat: Pattern
    replacement: str
    replacement_unsanitized: str
    in_use: bool = False
    new: bool = False
    modified: bool = False
    is_default: bool = False

    def __lt__(self, other: Any):
        if type(other) == TextMapping:
            if str(self.pat) == str(other.pat):
                if self.is_default == other.is_default:
                    return self.replacement < other.replacement
                else:
                    return not self.is_default

            return str(self.pat) < str(other.pat)

        if type(other) != TextMapping:
            raise ValueError(f"Unable to compare TextMapping against {type(other)}")


def text_mapping_representer(dumper: yaml.dumper.Dumper, data: TextMapping):
    return dumper.represent_mapping(
        "TextMapping",
        {
            "pat": data.pat.pattern,
            "replacement_unsanitized": data.replacement_unsanitized,
            "is_default": data.is_default,
        },
    )


def text_mapping_constructor(
    loader: Union[Loader, FullLoader, UnsafeLoader], node: yaml.Node
):
    value = loader.construct_mapping(node)  # type: ignore
    replacement_unsanitized = value["replacement_unsanitized"]
    return TextMapping(
        pat=re.compile(value["pat"]),
        replacement_unsanitized=replacement_unsanitized,
        replacement=sanitise_replacement(replacement_unsanitized),
        is_default=value["is_default"],
    )


yaml.add_representer(TextMapping, text_mapping_representer)
yaml.add_constructor("TextMapping", text_mapping_constructor)


def sanitise_replacement(original: str) -> str:
    return html.escape(original)


def parse_file(fp: Path, is_default: bool) -> List[TextMapping]:
    memo = []

    txt = fp.read_text()
    for l in txt.split("\n"):
        l = l.strip()
        if len(l) == 0:
            continue

        if l.startswith("#"):
            continue

        k, v = l.split("=")
        k = k.strip()
        v = v.strip()
        memo.append(
            TextMapping(
                pat=re.compile(k),
                replacement=sanitise_replacement(v),
                replacement_unsanitized=v,
                in_use=False,
                is_default=is_default,
            )
        )
    return memo


def load_mappings() -> List[TextMapping]:
    memo = []

    memo.extend(parse_file(vars.user_mappings, is_default=False))
    memo.extend(parse_file(vars.default_mappings, is_default=True))
    memo.sort()

    return memo


def save_mappings(mappings: List[TextMapping], dest: Path):
    with dest.open("wt") as fh:
        for m in mappings:
            fh.write(f"{m.pat.pattern} = {m.replacement_unsanitized}\n")


def export_mappings(
    mappings: List[TextMapping],
    default_version: VersionInfo,
    dest: Path,
):
    memo = {
        "mappings": mappings,
        "default_version": default_version,
    }

    dest.write_text(yaml.dump(memo))


def import_mappings(
    src: Path, user_mapping_dest: Path, default_mapping_dest: Path
) -> VersionInfo:
    memo = yaml.load(src.read_text(), Loader=yaml.Loader)
    mappings: List[TextMapping] = memo["mappings"]
    user_mappings = [m for m in mappings if not m.is_default]
    default_mappings = [m for m in mappings if m.is_default]

    save_mappings(user_mappings, user_mapping_dest)
    save_mappings(default_mappings, default_mapping_dest)

    return memo["default_version"]
