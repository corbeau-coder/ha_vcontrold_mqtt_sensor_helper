import pytest
from src.modules.xml_parser.xml_parser import CommandElement
from src.modules.template_engine.template_engine import YamlRenderer


import xml.etree.ElementTree as ET
from yaml import safe_load


testcases_CmdElements_template_good = [
    ("tests/template_engine/sample_files/sensor.yaml", "src/modules/template_engine/templates/sensor.jinja",[CommandElement(name="TestsensorTemp1",unittype="UT",desc="Temp Sensor")]),  
]


@pytest.mark.parametrize("sample_yaml, tmpl_path, input_list", testcases_CmdElements_template_good)
def test_yaml_samples(sample_yaml, tmpl_path, input_list):
    test_output = safe_load(YamlRenderer().generate_yaml(input_list, tmpl_path))
    with (open(sample_yaml, "r", encoding="utf-8") as fs):
        sample = safe_load(fs)
    assert test_output == sample