

test_xml_string_template_good = {
    "xml_string": "<?xml version=\"1.0\"?><vito><devices><device ID=\"2098\"/><device ID=\"2053\"/></devices><commands><command name=\"TestsensorTemp1\"> \
                    <addr>0800</addr><len>2</len><unit>UT</unit><description>Ermittle die Aussentemperatur in Grad C</description><device ID=\"2053\"> \
                    <addr>6F</addr><unit>UT1</unit><len>1</len></device></command></commands></vito>",
    "sample_file_name": "sample_files/sensor.yaml"}

def test_yaml_samples():
    #mocke input datei mit xml_string, asserte gegen geparsten Teil von sample_file_name
    pass