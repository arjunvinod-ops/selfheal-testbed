import pytest

from app.inventory import Inventory


@pytest.fixture
def inv():
    return Inventory(0.23, "EUR")


def test_add_and_total(inv):
    inv.add_item("A1", "widget", 2, 10.0)
    assert inv.total_value() == 24.6


def test_add_existing_sku_accumulates(inv):
    inv.add_item("A1", "widget", 2, 10.0)
    inv.add_item("A1", "widget", 3, 10.0)
    assert inv.total_value() == 61.5


def test_negative_quantity_rejected(inv):
    with pytest.raises(ValueError):
        inv.add_item("A1", "widget", -1, 10.0)


def test_remove_insufficient_stock(inv):
    inv.add_item("A1", "widget", 1, 10.0)
    with pytest.raises(ValueError):
        inv.remove_item("A1", 2)


def test_low_stock_excludes_items_at_threshold(inv):
    inv.add_item("A1", "widget", 5, 1.0)
    inv.add_item("B2", "gadget", 2, 1.0)
    assert inv.low_stock(5) == ["B2"]


def test_format_total(inv):
    inv.add_item("A1", "widget", 2, 10.0)
    assert inv.format_total() == "24.60 EUR"
