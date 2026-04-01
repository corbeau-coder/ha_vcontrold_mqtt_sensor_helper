from src.modules.xml_parser import CommandElement, TreeElement, XmlLoader, FileXmlLoader
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
def test_class_CommandElement_good(xml_element: ET.Element, expected_data):
    cut = CommandElement.fill_from_xml(xml_element)
    assert(cut.name == expected_data['name'])
    assert(cut.unittype == expected_data['unittype'])
    assert(cut.desc == expected_data['desc'])


expected_data = [(data, data) for data in test_data_bad]
@pytest.mark.parametrize("xml_element, expected_data", expected_data, indirect=["xml_element"])
def test_class_CommandElement_bad(xml_element: ET.Element, expected_data):
    with (pytest.raises(ValidationError) as exc):
       CommandElement.fill_from_xml(xml_element)
    assert exc.type is ValidationError


class FakeXmlLoader(XmlLoader):
    def __init__(self, xml_string: str):
        self.root = ET.fromstring(xml_string)
    def load(self, path: str) -> ET.Element:
        return self.root

@pytest.fixture
def fake_loader(request):
    data = request.param
    return FakeXmlLoader(data['xml_string'])

test_xml_string_good = [
    {"xml_string": "<?xml version=\"1.0\"?><vito><devices><device ID=\"2098\"/><device ID=\"2053\"/></devices><commands><command name=\"getTempA\"><addr>0800</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C</description><device ID=\"2053\"><addr>6F</addr><unit>UT1</unit><len>1</len></device></command><command name=\"getTempAtp\"><addr>5525</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C (Tiefpass)</description><device ID=\"2053\"/></command></commands></vito>",
     "expected_data": [{"name": "getTempA", "unittype": "UT", "desc": "Ermittle die Aussentemperatur in Grad C"},
                       {"name": "getTempAtp", "unittype": "UT", "desc": "Ermittle die Aussentemperatur in Grad C (Tiefpass)"}]},
]

expected_data = [(data['expected_data'],data) for data in test_xml_string_good]
@pytest.mark.parametrize("expected_data, fake_loader", expected_data, indirect=["fake_loader"])
def test_class_TreeElement_fetch_data_good(expected_data, fake_loader: FakeXmlLoader):
    path = ""
    cut = TreeElement.fetch_data(path, fake_loader)
    for i, item in enumerate(cut.cmd_list):
        assert item.name == expected_data[i]['name']
        assert item.unittype == expected_data[i]['unittype']
        assert item.desc == expected_data[i]['desc']



test_xml_string_devices_bad = [
    {"xml_string": ""},
    {"xml_string": "<?xml version=\"1.0\"?>"},
    {"xml_string": "<?xml version=\"1.0\"?><vito><comman"},
]

@pytest.fixture
def path_loader(request, tmp_path):
    data = request.param
    filename = str(tmp_path / "test.xml")
    with open(filename, "w") as f:
        f.write(data['xml_string'])
    
    return filename

@pytest.mark.parametrize("path_loader", test_xml_string_devices_bad, indirect=["path_loader"])
def test_class_FileXmlLoader_bad_content(path_loader):
    with (pytest.raises(ET.ParseError) as exc):    
        FileXmlLoader().load(path_loader)
    assert exc.type is ET.ParseError

def test_class_FileXmlLoader_bad_path():
    with (pytest.raises(FileNotFoundError) as exc):
        FileXmlLoader().load("")
    assert exc.type is FileNotFoundError


test_xml_string_devices_good = [
    {"xml_string": "<?xml version=\"1.0\"?><vito><devices><device ID=\"2098\"/><device ID=\"2053\"/></devices><commands><command name=\"getTempA\"><addr>0800</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C</description><device ID=\"2053\"><addr>6F</addr><unit>UT1</unit><len>1</len></device></command><command name=\"getTempAtp\"><addr>5525</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C (Tiefpass)</description><device ID=\"2053\"/></command></commands></vito>",
     "expected_data": "<vito><commands><command name=\"getTempA\"><addr>0800</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C</description></command><command name=\"getTempAtp\"><addr>5525</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C (Tiefpass)</description></command></commands></vito>"},
    {"xml_string": "<?xml version=\"1.0\"?><vito><commands><command name=\"getTempA\"><addr>0800</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C</description><device ID=\"2053\"><addr>6F</addr><unit>UT1</unit><len>1</len></device></command><command name=\"getTempAtp\"><addr>5525</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C (Tiefpass)</description><device ID=\"2053\"/></command></commands></vito>",
     "expected_data": "<vito><commands><command name=\"getTempA\"><addr>0800</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C</description></command><command name=\"getTempAtp\"><addr>5525</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C (Tiefpass)</description></command></commands></vito>"},
    {"xml_string": "<?xml version=\"1.0\"?><vito><commands><command name=\"getTempA\"><addr>0800</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C</description></command><command name=\"getTempAtp\"><addr>5525</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C (Tiefpass)</description></command></commands></vito>",
     "expected_data": "<vito><commands><command name=\"getTempA\"><addr>0800</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C</description></command><command name=\"getTempAtp\"><addr>5525</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C (Tiefpass)</description></command></commands></vito>"},
]

expected_data = [(data['expected_data'], data) for data in test_xml_string_devices_good]
@pytest.mark.parametrize("expected_string, fake_loader", expected_data, indirect=["fake_loader"])
def test_class_TreeElement_remove_device_references_good(expected_string: str, fake_loader: FakeXmlLoader):
    path = ""
    cut = TreeElement.fetch_data(path, fake_loader)
    cut.remove_dev_refs()
    assert ET.tostring(cut.root_elem, encoding='unicode', method='xml') == expected_string


