import pytest

from config import load_config


def test_load_default_config():
    cfg = load_config("config/app.yaml")
    assert cfg["pricing"]["tax_rate"] == 0.23
    assert cfg["service"]["port"] == 8085


def test_missing_key_raises(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("service:\n  name: x\n", encoding="utf-8")
    with pytest.raises(KeyError):
        load_config(str(path))
