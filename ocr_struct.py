from dataclasses import dataclass
from typing import Dict
import pyfury


@dataclass
class FunctionArguments:
    credentials: Dict[str, str]
    properties: Dict[str, str]

@dataclass
class Inputs:
    pdf: bytes

@dataclass
class Outputs:
    ocr_json: str
    raw_text: str

fruy_struct = pyfury.Fury()
fruy_struct.register_class(FunctionArguments, type_tag="FunctionArguments")
fruy_struct.register_class(Inputs, type_tag="Inputs")
fruy_struct.register_class(Outputs, type_tag="Outputs")
