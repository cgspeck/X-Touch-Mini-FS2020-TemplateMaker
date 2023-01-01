from pathlib import Path
from typing import List
import pytest
from template_maker.button import Button
from template_maker.encoder import Encoder

from template_maker.generator import generate_svgstr

EXPECTED_SVG_HAPPY_PATH = Path("tests", "data", "expected_svg_happy_path.svg")
EXPECTED_SVG_NO_DATA_PATH = Path("tests", "data", "expected_svg_no_data.svg")


@pytest.fixture()
def expected_svg_no_data() -> str:
    return EXPECTED_SVG_NO_DATA_PATH.read_text()


def save_expected_svg_no_data(s: str) -> None:
    EXPECTED_SVG_NO_DATA_PATH.write_text(s)


def test_generate_svgstr_no_data(expected_svg_no_data: str):
    encoders = [
        Encoder(1),
        Encoder(2),
        Encoder(3),
        Encoder(4),
        Encoder(5),
        Encoder(6),
        Encoder(7),
        Encoder(8),
    ]

    buttons = [
        Button(1),
        Button(2),
        Button(3),
        Button(4),
        Button(5),
        Button(6),
        Button(7),
        Button(8),
        Button(9),
        Button(10),
        Button(11),
        Button(12),
        Button(13),
        Button(14),
        Button(15),
        Button(16),
    ]
    actual = generate_svgstr(buttons, encoders)
    # uncomment to update snapshot
    # save_expected_svg_no_data(actual)
    assert actual == expected_svg_no_data


@pytest.fixture()
def expected_svg_happy() -> str:
    return EXPECTED_SVG_HAPPY_PATH.read_text()


def save_expected_svg_happy(s: str) -> None:
    EXPECTED_SVG_HAPPY_PATH.write_text(s)


def test_generate_svgstr_happy_path(expected_svg_happy: str):
    buttons = [
        Button(index=1, layer_a_text="FD"),
        Button(index=2, layer_a_text="HDG"),
        Button(index=3, layer_a_text="SPEED"),
        Button(index=4, layer_a_text="ALT"),
        Button(index=5, layer_a_text="VS"),
        Button(index=6, layer_a_text="BC"),
        Button(index=7, layer_a_text="TOGA"),
        Button(index=8, layer_a_text=None),
        Button(index=9, layer_a_text="AP"),
        Button(index=10, layer_a_text="NAV1"),
        Button(index=11, layer_a_text="A/THR"),
        Button(index=12, layer_a_text="FLC"),
        Button(index=13, layer_a_text="LOC AVAIL"),
        Button(index=14, layer_a_text="APPR"),
        Button(index=15, layer_a_text="YAW DPNR"),
        Button(index=16, layer_a_text=None),
    ]
    encoders = [
        Encoder(
            index=1,
            layer_a_primary_text="CRS",
            layer_a_secondary_text="",
            layer_a_tertiary_text=None,
        ),
        Encoder(
            index=2,
            layer_a_primary_text="HDG",
            layer_a_secondary_text="SET",
            layer_a_tertiary_text=None,
        ),
        Encoder(
            index=3,
            layer_a_primary_text="SPEED",
            layer_a_secondary_text=None,
            layer_a_tertiary_text=None,
        ),
        Encoder(
            index=4,
            layer_a_primary_text="ALT",
            layer_a_secondary_text=None,
            layer_a_tertiary_text=None,
        ),
        Encoder(
            index=5,
            layer_a_primary_text="VS",
            layer_a_secondary_text="ATT",
            layer_a_tertiary_text=None,
        ),
        Encoder(
            index=6,
            layer_a_primary_text="BARO",
            layer_a_secondary_text="SET",
            layer_a_tertiary_text=None,
        ),
        Encoder(
            index=7,
            layer_a_primary_text="COM",
            layer_a_secondary_text="",
            layer_a_tertiary_text="<->",
        ),
        Encoder(
            index=8,
            layer_a_primary_text="NAV1",
            layer_a_secondary_text="",
            layer_a_tertiary_text="<->",
        ),
    ]
    actual = generate_svgstr(buttons, encoders)
    # uncomment to update snapshot
    # save_expected_svg_happy(actual)
    assert actual == expected_svg_happy
