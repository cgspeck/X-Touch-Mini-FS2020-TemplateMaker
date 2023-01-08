from pathlib import Path
import pytest
from template_maker.button import Button, ButtonLabels
from template_maker.encoder import Encoder, EncoderLabels

from template_maker.generator_util import generate_svgstr
from template_maker.label import Label
from template_maker.text_mapping import sanitise_replacement

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
        Button(
            index=1,
            layer_a=ButtonLabels(
                primary=Label(
                    original="TOGGLE_FLIGHT_DIRECTOR", display="FD", replaced=True
                )
            ),
        ),
        Button(
            index=2,
            layer_a=ButtonLabels(
                primary=Label(original="AP_HDG_HOLD", display="HDG", replaced=True),
            ),
        ),
        Button(
            index=3,
            layer_a=ButtonLabels(
                primary=Label(
                    original="AP_AIRSPEED_HOLD", display="SPEED", replaced=True
                ),
            ),
        ),
        Button(
            index=4,
            layer_a=ButtonLabels(
                primary=Label(original="AP_ALT_HOLD", display="ALT", replaced=True),
            ),
        ),
        Button(
            index=5,
            layer_a=ButtonLabels(
                primary=Label(original="AP_VS_HOLD", display="VS", replaced=True),
            ),
        ),
        Button(
            index=6,
            layer_a=ButtonLabels(
                primary=Label(original="AP_BC_HOLD", display="BC", replaced=True),
            ),
        ),
        Button(
            index=7,
            layer_a=ButtonLabels(
                primary=Label(
                    original="AUTO_THROTTLE_TO_GA", display="TOGA", replaced=True
                ),
            ),
        ),
        Button(
            index=8,
            layer_a=ButtonLabels(
                primary=Label(original=None, display=None, replaced=False)
            ),
        ),
        Button(
            index=9,
            layer_a=ButtonLabels(
                primary=Label(original="AP_MASTER", display="AP", replaced=True),
            ),
        ),
        Button(
            index=10,
            layer_a=ButtonLabels(
                primary=Label(original="AP_NAV1_HOLD", display="NAV1", replaced=True),
            ),
        ),
        Button(
            index=11,
            layer_a=ButtonLabels(
                primary=Label(
                    original="AUTO_THROTTLE_ARM",
                    display=sanitise_replacement("A/THR"),
                    replaced=True,
                ),
            ),
        ),
        Button(
            index=12,
            layer_a=ButtonLabels(
                primary=Label(
                    original="FLIGHT_LEVEL_CHANGE", display="FLC", replaced=True
                ),
            ),
        ),
        Button(
            index=13,
            layer_a=ButtonLabels(
                primary=Label(
                    original="AP_LOC_HOLD", display="LOC AVAIL", replaced=True
                ),
            ),
        ),
        Button(
            index=14,
            layer_a=ButtonLabels(
                primary=Label(original="AP_APR_HOLD", display="APPR", replaced=True),
            ),
        ),
        Button(
            index=15,
            layer_a=ButtonLabels(
                primary=Label(
                    original="YAW_DAMPER_TOGGLE", display="YAW DPNR", replaced=True
                ),
            ),
        ),
        Button(
            index=16,
            layer_a=ButtonLabels(
                primary=Label(original=None, display=None, replaced=False)
            ),
        ),
    ]
    encoders = [
        Encoder(
            index=1,
            layer_a=EncoderLabels(
                primary=Label(original="VOR1_OBI_INC", display="CRS", replaced=True),
                secondary=Label(original="{alternate}", display="", replaced=True),
                tertiary=Label(original=None, display=None, replaced=False),
            ),
        ),
        Encoder(
            index=2,
            layer_a=EncoderLabels(
                primary=Label(original="HEADING_BUG_INC", display="HDG", replaced=True),
                secondary=Label(
                    original="HEADING_BUG_SET", display="SET", replaced=True
                ),
                tertiary=Label(original=None, display=None, replaced=False),
            ),
        ),
        Encoder(
            index=3,
            layer_a=EncoderLabels(
                primary=Label(
                    original="AP_SPD_VAR_INC", display="SPEED", replaced=True
                ),
                secondary=Label(original=None, display=None, replaced=False),
                tertiary=Label(original=None, display=None, replaced=False),
            ),
        ),
        Encoder(
            index=4,
            layer_a=EncoderLabels(
                primary=Label(original="AP_ALT_VAR_INC", display="ALT", replaced=True),
                secondary=Label(original=None, display=None, replaced=False),
                tertiary=Label(original=None, display=None, replaced=False),
            ),
        ),
        Encoder(
            index=5,
            layer_a=EncoderLabels(
                primary=Label(original="AP_VS_VAR_INC", display="VS", replaced=True),
                secondary=Label(original="AP_ATT_HOLD", display="ATT", replaced=True),
                tertiary=Label(original=None, display=None, replaced=False),
            ),
        ),
        Encoder(
            index=6,
            layer_a=EncoderLabels(
                primary=Label(original="KOHLSMAN_INC", display="BARO", replaced=True),
                secondary=Label(original="KOHLSMAN_SET", display="SET", replaced=True),
                tertiary=Label(original=None, display=None, replaced=False),
            ),
        ),
        Encoder(
            index=7,
            layer_a=EncoderLabels(
                primary=Label(
                    original="COM_RADIO_WHOLE_INC", display="COM", replaced=True
                ),
                secondary=Label(original="{alternate}", display="", replaced=True),
                tertiary=Label(
                    original="COM_STBY_RADIO_SWAP",
                    display=sanitise_replacement("<->"),
                    replaced=True,
                ),
            ),
        ),
        Encoder(
            index=8,
            layer_a=EncoderLabels(
                primary=Label(
                    original="NAV1_RADIO_WHOLE_INC", display="NAV1", replaced=True
                ),
                secondary=Label(original="{alternate}", display="", replaced=True),
                tertiary=Label(
                    original="NAV1_RADIO_SWAP",
                    display=sanitise_replacement("<->"),
                    replaced=True,
                ),
            ),
        ),
    ]
    actual = generate_svgstr(buttons, encoders)
    # uncomment to update snapshot
    # save_expected_svg_happy(actual)
    assert actual == expected_svg_happy
