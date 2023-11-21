from pathlib import Path
import json
from typing import Any, List, Mapping, Optional, Union

from template_maker.button import Button, ButtonLabels
from template_maker.datadefs import EventPressDefinition
from template_maker.label import Label
from template_maker.template_info import TemplateInfo
from template_maker.encoder import Encoder, EncoderLabels


def parse_event_press(
    blk: Optional[Union[str, List[str], Mapping[str, Any]]]
) -> EventPressDefinition:
    event = None
    value = None

    match blk:
        case str():
            event = blk
        case list():
            event = "_".join(blk)
        case dict():
            event = blk.get("event", None)
            value = blk.get("value", None)
            # n.b. the values are usually ints?
            if value is not None:
                value = str(value)
        case _:
            event = None

    return EventPressDefinition(event, value)


def parse_aircraft_config(filepath: Path) -> TemplateInfo:
    error_msgs: List[str] = []
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

    dct: Optional[Mapping[str, Any]] = None

    try:
        txt = filepath.read_text()
        dct = json.loads(txt)
    except FileNotFoundError:
        error_msgs.append(f"Unable to open file '{filepath}'")
    except OSError as err:
        error_msgs.append(f"Unable to open file '{filepath}'\n\n'{err}'")
    except (UnicodeDecodeError, json.JSONDecodeError):
        error_msgs.append(f"Invalid json file '{filepath}'")

    if dct is not None:
        if "encoders" in dct:
            for encoder_blk in dct["encoders"]:
                encoder_index = encoder_blk["index"]
                if encoder_index > 8 or encoder_index < 1:
                    continue

                list_index = encoder_index - 1
                primary_def = parse_event_press(encoder_blk.get("event_up", None))
                secondary_def = parse_event_press(encoder_blk.get("event_press", None))

                if secondary_def is None:
                    secondary_def = parse_event_press(
                        encoder_blk.get("event_short_press", None)
                    )

                tertiary_text = parse_event_press(
                    encoder_blk.get("event_long_press", None)
                )

                if tertiary_text == secondary_def or tertiary_text == primary_def:
                    tertiary_text = None

                if secondary_def == primary_def:
                    secondary_def = None

                encoders[list_index].layer_a = EncoderLabels(
                    primary=Label(primary_def),
                    secondary=Label(secondary_def),
                    tertiary=Label(tertiary_text),
                )

        else:
            error_msgs.append('"encoders" key not found')

        if "buttons" in dct:
            for button_blk in dct["buttons"]:
                button_index = button_blk["index"]
                if button_index > 16 or button_index < 1:
                    continue

                list_index = button_index - 1
                primary_def = parse_event_press(button_blk.get("event_press", None))

                if primary_def is None:
                    primary_def = parse_event_press(
                        button_blk.get("event_short_press", None)
                    )

                secondary_def = parse_event_press(
                    button_blk.get("event_long_press", None)
                )

                if secondary_def == primary_def:
                    secondary_def = None

                buttons[list_index].layer_a = ButtonLabels(
                    primary=Label(primary_def), secondary=Label(secondary_def)
                )
        else:
            error_msgs.append('"buttons" key not found')

    return TemplateInfo(
        buttons=buttons, encoders=encoders, filepath=filepath, error_msgs=error_msgs
    )
