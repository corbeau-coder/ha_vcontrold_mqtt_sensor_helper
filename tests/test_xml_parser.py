from src.modules.xml_parser import CommandElement
import xml.etree.ElementTree as ET
import pytest
from pydantic import ValidationError

test_data_good = [
    {"name": "test_ele_0", "unittype": "UT", "desc": "test type UT"},
    {"name": "test_ele_1", "unittype": "PR", "desc": "test type PR"},
    {"name": "test_ele_2", "unittype": "ST", "desc": "test type ST"},
    {"name": "test_ele_3", "unittype": "CO", "desc": "test type CO"},
    {"name": "test_ele_4", "unittype": "CS", "desc": "test type CS"},
    {"name": "test_ele_5", "unittype": "CT", "desc": "test type CT"},
    {"name": "test_ele_6", "unittype": "BA", "desc": "test type BA"},
    {"name": "test_ele_7", "unittype": "SR", "desc": "test type SR"},
    {"name": "test_ele_8", "unittype": "TI", "desc": "test type TI"},
    {"name": "test_ele_9", "unittype": "ES", "desc": "test type ES"},
    {"name": "test_ele_10", "unittype": "RT", "desc": "test type RT"}
]

test_data_bad = [
    {"name": None, "unittype": "UT", "desc": "test type UT"},
    {"name": "test_bad_1", "unittype": None, "desc": "test type PR"},
    {"name": "test_bad_2", "unittype": "ST", "desc": None},
    {"name": "test_bad_1", "unittype": None, "desc": None},
    {"name": None, "unittype": None, "desc": None}
]

@pytest.fixture
def xml_element(request):
    data = request.param

    element = ET.Element('command', {'name':data['name']})
    ET.SubElement(element, "unit").text = data['unittype']
    ET.SubElement(element, "description").text = data['desc']

    return element


expected_data = [(data, data) for data in test_data_good]
@pytest.mark.parametrize("xml_element, expected_data", expected_data, indirect=["xml_element"])
def test_class_CommandElement_good_path(xml_element: ET.Element, expected_data):
    cot = CommandElement.fill_from_xml(xml_element)
    assert(cot.name == expected_data['name'])
    assert(cot.unittype == expected_data['unittype'])
    assert(cot.desc == expected_data['desc'])


expected_data = [(data, data) for data in test_data_bad]
@pytest.mark.parametrize("xml_element, expected_data", expected_data, indirect=["xml_element"])
def test_class_CommandElement_bad_path(xml_element: ET.Element, expected_data):
    with (pytest.raises(ValidationError) as exc):
       CommandElement.fill_from_xml(xml_element)
    assert exc.type is ValidationError