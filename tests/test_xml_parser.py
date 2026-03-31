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

    element = ET.Element('command')
    ET.SubElement(element, "name").text = data['name']
    ET.SubElement(element, "unit").text = data['unittype']
    ET.SubElement(element, "description").text = data['desc']

    return element


data = [(data, data) for data in test_data]
@pytest.mark.parametrize("xml_element, data", data, indirect=["xml_element"])
def test_class_CommandElement(xml_element: ET.Element, data):
    cot = CommandElement(xml_element)
    assert(cot.name == data['name'])
    assert(cot.unittype == data['unittype'])
    assert(cot.desc == data['desc']) 