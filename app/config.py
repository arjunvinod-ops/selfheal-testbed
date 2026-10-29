"""Configuration loading for the inventory service."""
import os

import yaml

REQUIRED_KEYS = (
    "service.name",
    "service.port",
    "service.health_path",
    "pricing.tax_rate",
    "pricing.currency",
)


def load_config(path=None):
    path = path or os.environ.get("APP_CONFIG", "config/app.yaml")
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    for dotted in REQUIRED_KEYS:
        node = data
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                raise KeyError(f"missing required config key: {dotted}")
            node = node[part]
    return data


if __name__ == "__main__":
    cfg = load_config()
    print(f"config OK: service={cfg['service']['name']} port={cfg['service']['port']}")
if __name__ == "__main__":
    cfg = load_config()
    print(f"config OK: service={cfg['service']['name']} port={cfg['service']['port']}")
