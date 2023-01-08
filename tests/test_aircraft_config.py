from pathlib import Path

import pytest
from pytest_insta import SnapshotFixture

from template_maker.aircraft_config import parse_aircraft_config


@pytest.fixture()
def config_generic_ap() -> str:
    return Path("tests", "data", "config_generic_ap.json")


@pytest.fixture()
def config_a320() -> str:
    return Path("tests", "data", "config_a320_modded.json")


def test_parse_generic_ap(config_generic_ap: str, snapshot: SnapshotFixture) -> None:
    actual = parse_aircraft_config(config_generic_ap).to_dict()
    assert snapshot("json") == actual


def test_dedupes_strings(config_a320: str) -> None:
    actual = parse_aircraft_config(config_a320)

    encoder1 = actual.encoders[0]
    assert encoder1.layer_a_primary_text.original == "KOHLSMAN_INC"
    assert encoder1.layer_a_secondary_text.original is None
    assert encoder1.layer_a_tertiary_text.original is None

    encoder2 = actual.encoders[1]
    assert encoder2.layer_a_primary_text.original == "AP_SPD_VAR_INC"
    assert encoder2.layer_a_secondary_text.original == "SPEED_SLOT_INDEX_SET"
    assert encoder2.layer_a_tertiary_text.original is None

    encoder3 = actual.encoders[2]
    assert encoder3.layer_a_primary_text.original == "HEADING_BUG_INC"
    assert encoder3.layer_a_secondary_text.original == "HEADING_SLOT_INDEX_SET"
    assert encoder3.layer_a_tertiary_text.original is None

    encoder4 = actual.encoders[3]
    assert encoder4.layer_a_primary_text.original == "AP_ALT_VAR_INC"
    assert encoder4.layer_a_secondary_text.original is None
    assert encoder4.layer_a_tertiary_text.original == "ALTITUDE_SLOT_INDEX_SET"

    encoder5 = actual.encoders[4]
    assert encoder5.layer_a_primary_text.original == "FOO"
    assert encoder5.layer_a_secondary_text.original == "BAR"
    assert encoder5.layer_a_tertiary_text.original is None
