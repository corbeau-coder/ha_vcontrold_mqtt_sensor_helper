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
    name_element = ET.SubElement(element, "name")
    name_element.text = data['name']
    ut_element = ET.SubElement(element, "unit")
    ut_element.text = data['unittype']
    desc_element = ET.SubElement(element, "description")
    desc_element.text = data['desc']

    return element



@pytest.mark.parametrize("xml_element, data", test_data, test_data, indirect=True)
def test_class_CommandElement(xml_element: ET.Element, data):
    cot = CommandElement(xml_element)
    assert(cot.name == data['name'])
    assert(cot.unittype == data['unittype'])
    assert(cot.desc == data['desc']) 