from pathlib import Path

import pytest
from pytest_insta import SnapshotFixture

from template_maker.aircraft_config import parse_aircraft_config


@pytest.fixture()
def config_generic_ap() -> Path:
    return Path("tests", "data", "config_generic_ap.json")


@pytest.fixture()
def config_a320() -> Path:
    return Path("tests", "data", "config_a320_modded.json")


def test_parse_generic_ap(config_generic_ap: Path, snapshot: SnapshotFixture) -> None:
    actual = parse_aircraft_config(config_generic_ap).to_dict()
    assert snapshot("json") == actual


def test_dedupes_strings(config_a320: Path) -> None:
    actual = parse_aircraft_config(config_a320)

    encoder1 = actual.encoders[0]
    assert encoder1.layer_a.primary.original == "KOHLSMAN_INC"  # type: ignore
    assert encoder1.layer_a.secondary.original is None  # type: ignore
    assert encoder1.layer_a.tertiary.original is None  # type: ignore

    encoder2 = actual.encoders[1]
    assert encoder2.layer_a.primary.original == "AP_SPD_VAR_INC"  # type: ignore
    assert encoder2.layer_a.secondary.original == "SPEED_SLOT_INDEX_SET"  # type: ignore
    assert encoder2.layer_a.tertiary.original is None  # type: ignore

    encoder3 = actual.encoders[2]
    assert encoder3.layer_a.primary.original == "HEADING_BUG_INC"  # type: ignore
    assert encoder3.layer_a.secondary.original == "HEADING_SLOT_INDEX_SET"  # type: ignore
    assert encoder3.layer_a.tertiary.original is None  # type: ignore

    encoder4 = actual.encoders[3]
    assert encoder4.layer_a.primary.original == "AP_ALT_VAR_INC"  # type: ignore
    assert encoder4.layer_a.secondary.original is None  # type: ignore
    assert encoder4.layer_a.tertiary.original == "ALTITUDE_SLOT_INDEX_SET"  # type: ignore

    encoder5 = actual.encoders[4]
    assert encoder5.layer_a.primary.original == "FOO"  # type: ignore
    assert encoder5.layer_a.secondary.original == "BAR"  # type: ignore
    assert encoder5.layer_a.tertiary.original is None  # type: ignore
