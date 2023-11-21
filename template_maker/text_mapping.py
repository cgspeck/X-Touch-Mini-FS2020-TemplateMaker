from __future__ import annotations
import html
import re
from dataclasses import dataclass, field
from pathlib import Path
from re import Pattern
import shutil
from typing import Any, List, Optional, Union

import yaml
from dataclasses_json import DataClassJsonMixin
from semver import VersionInfo
from yaml import FullLoader, Loader, UnsafeLoader

from template_maker import vars
from template_maker.logger import get_logger

DEFAULT_REPLACEMENT_TEXT = "SET ME!"

logger = get_logger()

SCHEMA_VERSION = VersionInfo(2, 0, 0)


@dataclass
class SerializedMappingCollection:
    mappings: List[TextMapping]
    schema_version: VersionInfo


@dataclass
class TextMapping(DataClassJsonMixin):
    pat: Pattern
    value_pat: Optional[Pattern]
    replacement: str
    replacement_unsanitized: str
    in_use: bool = False
    new: bool = False
    modified: bool = False
    is_default: bool = False
    deletable: bool = field(init=False)
    delete: bool = False

    def __post_init__(self):
        self.deletable = not self.is_default

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
            "value_pat": data.value_pat,
            "replacement_unsanitized": data.replacement_unsanitized,
            "is_default": data.is_default,
        },
    )


def text_mapping_constructor(
    loader: Union[Loader, FullLoader, UnsafeLoader], node: yaml.Node
):
    value = loader.construct_mapping(node)  # type: ignore
    replacement_unsanitized = value["replacement_unsanitized"]

    value_pat = value["value_pat"]
    if value_pat is not None:
        value_pat = re.compile(value_pat)

    return TextMapping(
        pat=re.compile(value["pat"]),
        value_pat=value_pat,
        replacement_unsanitized=replacement_unsanitized,
        replacement=sanitise_replacement(replacement_unsanitized),
        is_default=value["is_default"],
    )


yaml.add_representer(TextMapping, text_mapping_representer)
yaml.add_constructor("TextMapping", text_mapping_constructor)


def sanitise_replacement(original: str) -> str:
    return html.escape(original)


def _legacy_parse_user_txt_file() -> List[TextMapping]:
    fp = vars.user_mappings_legacy
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
                value_pat=None,
                replacement=sanitise_replacement(v),
                replacement_unsanitized=v,
                in_use=False,
                is_default=False,
            )
        )
    return memo


def _parse_defaults_yaml_file() -> List[TextMapping]:
    fp = vars.default_mappings
    memo = []
    dct = yaml.load(fp.read_text(), Loader=yaml.Loader)
    must_update = False
    for mapping in dct["mappings"]:
        match mapping:
            case str():
                logger.info("Parsing legacy default mapping definition")
                mapping = mapping.strip()
                if len(mapping) == 0:
                    continue

                k, v = mapping.split("=")
                k = k.strip()
                v = v.strip()
                memo.append(
                    TextMapping(
                        pat=re.compile(k),
                        value_pat=None,
                        replacement=sanitise_replacement(v),
                        replacement_unsanitized=v,
                        in_use=False,
                        is_default=True,
                    )
                )
                must_update = True
            case TextMapping():
                memo.append(mapping)
            case _:
                raise ValueError(f"Unexpected type for mapping block: ${type(mapping)}")

    if must_update:
        logger.info("Updating defaults file to new version...")
        mappings_version = get_default_mapping_version()
        save_default_mappings(memo, mappings_version, vars.default_mappings)

    return memo


def load_mappings() -> List[TextMapping]:
    memo = []

    if vars.user_mappings_legacy.exists():
        try:
            memo.extend(_legacy_parse_user_txt_file())
        except Exception as e:
            logger.error("Error loading legacy user mapping file", e)
        else:
            logger.info("Upgrading legacy mappings...")
            save_user_mappings(memo, vars.user_mappings)
        finally:
            logger.error("Deleting legacy mapping file")
            vars.user_mappings_legacy.unlink()
    elif vars.user_mappings.exists():
        try:
            logger.info("Loading user mappings")
            memo.extend(load_user_mappings(vars.user_mappings))
        except Exception as e:
            logger.error("Error loading user mapping file", e)

    if not vars.default_mappings.exists():
        shutil.copy(vars.default_mappings_dist, vars.default_mappings)
        logger.info("Default mappings were restored from dist file")

    memo.extend(_parse_defaults_yaml_file())
    memo.sort()

    return memo


def save_user_mappings(mappings: List[TextMapping], dest: Path):
    memo = SerializedMappingCollection(mappings, SCHEMA_VERSION)
    dest.write_text(yaml.dump(memo))


def load_user_mappings(src: Path) -> List[TextMapping]:
    if src is None:
        src = vars.user_mappings

    memo: SerializedMappingCollection = yaml.load(src.read_text(), Loader=yaml.Loader)
    return memo.mappings


def save_default_mappings(
    mappings: List[TextMapping], version: VersionInfo, dest: Path
):
    memo = {
        "version": version,
        "mappings": mappings,
    }
    dest.write_text(yaml.dump(memo))


def get_default_mapping_version():
    return yaml.load(vars.default_mappings.read_text(), Loader=yaml.Loader)["version"]


def export_mappings(
    mappings: List[TextMapping],
    dest: Path,
):
    memo = {
        "mappings": mappings,
        "default_version": get_default_mapping_version(),
    }

    dest.write_text(yaml.dump(memo))


def import_mappings(
    src: Path, user_mapping_dest: Path, default_mapping_dest: Path
) -> VersionInfo:
    memo = yaml.load(src.read_text(), Loader=yaml.Loader)
    mappings: List[TextMapping] = memo["mappings"]
    version: VersionInfo = memo["default_version"]
    user_mappings = [m for m in mappings if not m.is_default]
    default_mappings = [m for m in mappings if m.is_default]

    save_user_mappings(user_mappings, user_mapping_dest)
    save_default_mappings(default_mappings, version, default_mapping_dest)

    return version
