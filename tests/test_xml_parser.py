from src.modules.xml_parser import CommandElement
import xml.etree.ElementTree as ET
import pytest

test_data = [
    {"name": "asd", "unittype": "DASDAS", "desc": "asdasd"},
    {"name": "asd", "unittype": "DASDAS", "desc": "asdasd"},
    {"name": "asd", "unittype": "DASDAS", "desc": "asdasd"}
]

@pytest.fixture
def xml_element(request):
    data = request.param

    element = ET.Element('command', {'name':data['name']})
    ET.SubElement(element, "unit").text = data['unittype']
    ET.SubElement(element, "description").text = data['desc']

    return element


expected_data = [(data, data) for data in test_data]
@pytest.mark.parametrize("xml_element, expected_data", expected_data, indirect=["xml_element"])
def test_class_CommandElement(xml_element: ET.Element, expected_data):
    cot = CommandElement(xml_element)
    assert(cot.name == expected_data['name'])
    assert(cot.unittype == expected_data['unittype'])
    assert(cot.desc == expected_data['desc'])