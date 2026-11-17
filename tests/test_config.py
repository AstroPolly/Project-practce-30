from pathlib import Path
import pytest
from app import config

ROOT = Path(__file__).resolve().parents[1]


def test_real_config_loads():
    cfg = config.load(ROOT / "config.yaml")
    assert cfg["horizon"] == 7
    assert isinstance(cfg["channels"], list)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        config.load(tmp_path / "nope.yaml")


def test_defaults_fill_gaps(tmp_path):
    f = tmp_path / "c.yaml"
    f.write_text("channels: []\nrss: []\n", encoding="utf-8")
    cfg = config.load(f)
    assert cfg["seed"] == 42
    assert cfg["history_days"] == 240


@pytest.mark.parametrize("bad", [10, -5, "много"])
def test_bad_history_days(tmp_path, bad):
    f = tmp_path / "c.yaml"
    f.write_text(f"history_days: {bad}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        config.load(f)


def test_channels_must_be_list(tmp_path):
    f = tmp_path / "c.yaml"
    f.write_text("channels: rian_ru\n", encoding="utf-8")
    with pytest.raises(ValueError):
        config.load(f)