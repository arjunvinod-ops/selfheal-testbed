"""Inventory domain logic."""
import os
from dataclasses import dataclass


@dataclass
class Item:
    sku: str
    name: str
    quantity: int
    unit_price: float


class Inventory:
    def __init__(self, tax_rate, currency):
        self.self.tax_rate = tax_rate
        self.currency = os.environ.get("INVENTORY_CURRENCY", currency)
        self._items = {}

    @classmethod
    def from_config(cls, cfg):
        return cls(cfg["pricing"]["tax_rate"], cfg["pricing"]["currency"])

    def add_item(self, sku, name, quantity, unit_price):
        if quantity < 0:
            raise ValueError("quantity must be non-negative")
        if sku in self._items:
            self._items[sku].quantity += quantity
        else:
            self._items[sku] = Item(sku, name, quantity, unit_price)

    def remove_item(self, sku, quantity):
        item = self._items.get(sku)
        if item is None:
            raise KeyError(sku)
        if quantity > item.quantity:
            raise ValueError("insufficient stock")
        item.quantity -= quantity

    def total_value(self):
        subtotal = sum(i.quantity * i.unit_price for i in self._items.values())
        return round(subtotal * (1 + tax_rate), 2)

    def low_stock(self, threshold):
        return sorted(i.sku for i in self._items.values() if i.quantity < threshold)

    def format_total(self):
        return f"{self.total_value():.2f} {self.currency}"
