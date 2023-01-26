from __future__ import annotations

import re
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import List

from pytest_insta import SnapshotFixture
from semver import VersionInfo

from template_maker.text_mapping import TextMapping, export_mappings, import_mappings


class AugmentedStringIo(StringIO):
    @contextmanager
    def open(self, _flags: str):
        yield self

    def write_text(self, s: str):
        self.write(s)


def test_export_mappings(snapshot: SnapshotFixture):
    mappings: List[TextMapping] = [
        TextMapping(
            pat=re.compile("pattern 1"),
            replacement="replacement 1",
            replacement_unsanitized="unsanitised replacement 1",
            is_default=False,
        ),
        TextMapping(
            pat=re.compile("pattern 2"),
            replacement="replacement 2",
            replacement_unsanitized="unsanitised replacement 2",
            is_default=True,
        ),
    ]
    default_version = VersionInfo(1, 2, 3)
    dest = AugmentedStringIo()
    export_mappings(mappings, default_version, dest)  # type: ignore
    dest.seek(0)
    actual = dest.read()
    assert snapshot("txt") == actual


def test_import_mappings(snapshot: SnapshotFixture):
    user_mapping_dst = AugmentedStringIo()
    default_mapping_dst = AugmentedStringIo()
    src = Path("tests", "data", "exported_mappings.yaml")
    default_mapping_ver = import_mappings(src, user_mapping_dst, default_mapping_dst)  # type: ignore
    assert default_mapping_ver == VersionInfo(1, 2, 3)
    user_mapping_dst.seek(0)
    assert snapshot("txt") == user_mapping_dst.read()
    default_mapping_dst.seek(0)
    assert snapshot("txt") == default_mapping_dst.read()
