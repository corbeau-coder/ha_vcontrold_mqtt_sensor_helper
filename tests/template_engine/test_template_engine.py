import pytest
from unittest.mock import mock_open

import xml.etree.ElementTree as ET
from yaml import safe_load


test_CmdElements_template_good = [
    {
    }
]



#test_data = {(data["xml_string"], data["sample_file_name"]) for data in test_CmdElements_template_good}
#@pytest.mark.parametrize("input_xml, output_yaml", test_data)
def test_yaml_samples():
    #main(input_xml) mock den inputzugriff in main, vermutlich xml_parser.CommandElement.fetch_data sowie TreeElement.fill_from_xml
    #assert output_yaml mit dem geschriebenen output aus template_engine.write_output_to_file()
    
    pass