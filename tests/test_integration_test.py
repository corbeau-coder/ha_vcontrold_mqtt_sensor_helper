import pytest

from unittest.mock import patch

from src.yaml_mqtt_vcontrold_helper import main


def fake_exit(code):
    raise SystemExit(code)

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
def test_argumented_flow(monkeypatch, arguments, exit_code, expected_outcome):
    with (patch("src.yaml_mqtt_vcontrold_helper.logger") as logger_mock):
        monkeypatch.setattr("sys.argv", arguments)
        monkeypatch.setattr("sys.exit", fake_exit)

        with (pytest.raises(SystemExit) as exc):
            main("")
        assert exc.value.code == exit_code
        if expected_outcome is not None:
            for ele in expected_outcome:
                logger_mock.info.assert_any_call(ele)
    


#del_refs
#create config yaml
#verbose
#invalid/empty - übersicht