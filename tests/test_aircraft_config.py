import json
from pathlib import Path
from pprint import pprint

import pytest
from pytest_insta import SnapshotFixture

from template_maker.aircraft_config import parse_aircraft_config
from template_maker.datadefs import EventPressDefinition


@pytest.fixture()
def config_generic_ap() -> Path:
    return Path("tests", "data", "config_generic_ap.json")


@pytest.fixture()
def config_a320() -> Path:
    return Path("tests", "data", "config_a320_modded.json")


def test_parse_generic_ap(config_generic_ap: Path, snapshot: SnapshotFixture) -> None:
    actual = parse_aircraft_config(config_generic_ap).to_dict()
    assert snapshot("json") == actual


def test_dedupes_strings(config_a320: Path, snapshot: SnapshotFixture) -> None:
    actual = parse_aircraft_config(config_a320)

    encoder_dicts = [e.to_dict() for e in actual.encoders if e is not None]
    assert snapshot("json") == encoder_dicts
