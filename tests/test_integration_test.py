import pytest

from unittest.mock import patch, mock_open, MagicMock
import xml.etree.ElementTree as ET

from src.yaml_mqtt_vcontrold_helper import main


def fake_exit(code):
    raise SystemExit(code)

1
test_xml_file_strings = {
    "vito_before":"<vito><devices><device/><device id=\"1337\"><unit>UT</unit></device></devices>"
                  "<commands><command name=\"getTempA\"><unit>UT</unit><description>get Temp A</description></command>"
                  "<command name=\"getTempAtp\"><len>1</len><device id=\"4242\"><addr>FF</addr></device><unit>UT</unit><description>get Temp A tp</description></command></commands></vito>",
    "vito_after":"<vito>"
                  "<commands><command name=\"getTempA\"><unit>UT</unit><description>get Temp A</description></command>"
                  "<command name=\"getTempAtp\"><len>1</len><unit>UT</unit><description>get Temp A tp</description></command></commands></vito>",
    "conf_after":""}

@pytest.fixture
def mock_xml_file():
    mock_tree = MagicMock()
    mock_tree.getroot.return_value = ET.fromstring(test_xml_file_strings["vito_before"])
    mock_storer = MagicMock()

    with (patch("src.modules.xml_parser.xml_parser.ET.parse", return_value=mock_tree),
          patch("builtins.open", mock_open(read_data=test_xml_file_strings["vito_before"])),
          patch("src.modules.xml_parser.xml_parser.FileXmlStorer.store", mock_storer)):
        yield "fake/path.xml", mock_storer

@pytest.mark.parametrize("arguments, exit_code, expected_outcome", [
    (["yaml_mqtt_vcontrold_helper.py", ""], 2, None),
    (["yaml_mqtt_vcontrold_helper.py", "-c"], 0, ["done. Created configuration.yaml sucessfully"]),
    (["yaml_mqtt_vcontrold_helper.py", "-d"], 0, ["done. Removed all device elements in vito.xml"]),
    (["yaml_mqtt_vcontrold_helper.py", "-v"], 0, ["verbose output enabled"]),
    (["yaml_mqtt_vcontrold_helper.py", "-c" ,"-v"], 0, ["verbose output enabled", "done. Created configuration.yaml sucessfully"]),
    (["yaml_mqtt_vcontrold_helper.py", "-d" ,"-v"], 0, ["verbose output enabled", "done. Removed all device elements in vito.xml"]),
    (["yaml_mqtt_vcontrold_helper.py", "-c" ,"-v", "-d"], 0, ["verbose output enabled", "done. Created configuration.yaml sucessfully", "done. Removed all device elements in vito.xml"]),
    (["yaml_mqtt_vcontrold_helper.py", "-d" , "-c"], 0, ["done. Created configuration.yaml sucessfully", "done. Removed all device elements in vito.xml"]),
])
def test_argumented_flow_good(monkeypatch, arguments, exit_code, expected_outcome, mock_xml_file):
    path, mock_storer = mock_xml_file
    with (patch("src.yaml_mqtt_vcontrold_helper.logger") as logger_mock):
        monkeypatch.setattr("sys.argv", arguments)
        monkeypatch.setattr("sys.exit", fake_exit)

        with (pytest.raises(SystemExit) as exc):
            main(path)
        assert exc.value.code == exit_code
        if expected_outcome is not None:
            for ele in expected_outcome:
                logger_mock.info.assert_any_call(ele)
        if "-d" in arguments:
            written_elem = mock_storer.call_args[0][1]
            assert ET.tostring(written_elem, encoding="unicode") == test_xml_file_strings["vito_after"]
    


#create config yaml
#verbose
#invalid/empty - übersicht
