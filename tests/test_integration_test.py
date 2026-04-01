import pytest
from src.yaml_mqtt_vcontrold_helper import main


def fake_exit(code):
    raise SystemExit(code)

@pytest.mark.parametrize("arguments, exit_code, expected_outcome", [
    (["yaml_mqtt_vcontrold_helper.py", ""], 2, ""),
    (["yaml_mqtt_vcontrold_helper.py", "-c"], 0, ""),
    (["yaml_mqtt_vcontrold_helper.py", "-d"], 0, ""),
])
def test_argumented_flow(monkeypatch, arguments, exit_code, expected_outcome):
    monkeypatch.setattr("sys.argv", arguments)
    monkeypatch.setattr("sys.exit", fake_exit)

    with (pytest.raises(SystemExit) as exc):
        main("")
    assert exc.value.code == exit_code


#del_refs
#create config yaml
#verbose
#invalid/empty - übersicht