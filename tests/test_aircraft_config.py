from pathlib import Path

import pytest
from pytest_insta import SnapshotFixture

from template_maker.aircraft_config import parse_aircraft_config


@pytest.fixture()
def config_generic_ap() -> str:
    return Path("tests", "data", "config_generic_ap.json")


def test_parse_generic_ap(config_generic_ap: str, snapshot: SnapshotFixture) -> None:
    assert snapshot("json") == parse_aircraft_config(config_generic_ap).to_dict()
