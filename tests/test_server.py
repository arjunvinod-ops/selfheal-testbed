import json
import threading
import urllib.request

import pytest

from app.inventory import Inventory
from app.server import create_server


@pytest.fixture
def base_url():
    inv = Inventory(0.23, "EUR")
    inv.add_item("A1", "widget", 2, 10.0)
    server = create_server(inv, "127.0.0.1", 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def test_health_responds_quickly(base_url):
    with urllib.request.urlopen(f"{base_url}/health", timeout=1) as resp:
        assert json.load(resp) == {"status": "ok"}


def test_items_total(base_url):
    with urllib.request.urlopen(f"{base_url}/items", timeout=1) as resp:
        assert json.load(resp) == {"total": "24.6 EUR"}
