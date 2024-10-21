from dataclasses import dataclass, field
from typing import List


@dataclass
class ItemInfo:
    name: str
    price: float
    deleted: bool = False


@dataclass
class Item:
    id: int
    info: ItemInfo


@dataclass
class CartItem:
    id: int
    name: str
    quantity: int
    available: bool


@dataclass
class CartInfo:
    items: List[CartItem | None] = field(default_factory=list)
    price: float = 0.0


@dataclass
class Cart:
    id: int
    info: CartInfo
