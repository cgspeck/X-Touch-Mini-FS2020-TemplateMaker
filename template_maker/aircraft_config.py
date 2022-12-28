
from pathlib import Path
import json
from typing import Any, List, Mapping, Optional, Union

from template_maker.button import Button
from template_maker.template_info import TemplateInfo
from template_maker.encoder import Encoder

def parse_event_press(blk: Optional[Union[str, List[str], Mapping[str, Any]]]) -> Optional[str]:
    if blk is None:
        return None

    if type(blk) == str:
        return blk
    
    if type(blk) == list and len(blk) > 0:
        return '_'.join(blk)

    return blk.get('event', None)

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
    except (UnicodeDecodeError, json.JSONDecodeError):
        error_msgs.append(f"Invalid json file '{filepath}'")
    
    if dct is not None:
        if 'encoders' in dct:
            for encoder_blk in dct['encoders']:
                encoder_index = encoder_blk['index']
                if encoder_index > 8 or encoder_index < 1:
                    continue

                list_index = encoder_index - 1
                primary_text = encoder_blk.get('event_up', None)
                secondary_text = parse_event_press(encoder_blk.get('event_press', None))

                encoders[list_index].layer_a_primary_text = primary_text
                encoders[list_index].layer_a_secondary_text = secondary_text
        else:
            error_msgs.append('"encoders" key not found')

        if 'buttons' in dct:
                for button_blk in dct['buttons']:
                    button_index = button_blk['index']
                    if button_index > 16 or button_index < 1:
                        continue

                    list_index = button_index - 1
                    layer_a_text = parse_event_press(button_blk.get('event_press', None))
                    buttons[list_index].layer_a_text = layer_a_text
        else:
            error_msgs.append('"buttons" key not found')

    return TemplateInfo(
        buttons=buttons,
        encoders=encoders,
        filepath=filepath,
        error_msgs=error_msgs
    )
