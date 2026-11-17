"""Config for whole application."""
from pathlib import Path
import yaml

DEFAULTS = {
    "db_path": "data/observatory.db",
    "history_days": 240,
    "horizon": 7,
    "seed": 42,
    "channels": [],
    "rss": [],
    "telegram": {"session": "data/tg"},
}

REQUIRED = ("db_path", "history_days", "horizon", "seed", "channels", "rss")


def load(path="config.yaml"):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Нет файла настроек: {p}")
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    cfg = {**DEFAULTS, **raw}          # чего нет в файле — берём из значений по умолчанию
    check(cfg)
    return cfg


def check(cfg):
    for key in REQUIRED:
        if key not in cfg:
            raise ValueError(f"В настройках нет обязательного поля: {key}")

    if not isinstance(cfg["history_days"], int) or cfg["history_days"] < 30:
        raise ValueError("history_days: нужно целое число не меньше 30")

    if not isinstance(cfg["horizon"], int) or not 1 <= cfg["horizon"] <= 30:
        raise ValueError("horizon: нужно целое число от 1 до 30")

    if not isinstance(cfg["seed"], int) or cfg["seed"] < 0:
        raise ValueError("seed: нужно целое неотрицательное число")

    if not isinstance(cfg["channels"], list):
        raise ValueError("channels: должен быть список адресов каналов")

    if not isinstance(cfg["rss"], list):
        raise ValueError("rss: должен быть список ссылок")

    for ch in cfg["channels"]:
        if not isinstance(ch, str) or not ch.strip():
            raise ValueError("Адрес канала должен быть непустой строкой")

    return True