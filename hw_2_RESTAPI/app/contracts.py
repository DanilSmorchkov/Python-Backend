from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Literal

from hw_2_RESTAPI.store.models import Item, ItemInfo, CartItem, Cart


# contracts for items
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    # deleted: bool # Непонятно, нужно ли выводить данное поле

    @staticmethod
    def from_item(model: Item) -> ItemResponse:
        return ItemResponse(
            id=model.id,
            name=model.info.name,
            price=model.info.price,
            # deleted=model.info.deleted,
        )


class ItemRequest(BaseModel):
    name: str
    price: Annotated[float, Field(gt=0.0)]
    deleted: bool = False

    def to_item_info(self) -> ItemInfo:
        return ItemInfo(name=self.name, price=self.price, deleted=self.deleted)


class PatchItemRequest(BaseModel):
    name: str = None
    price: Annotated[float, Field(gt=0.0)] = None

    model_config = ConfigDict(extra='forbid')

    def to_item_info(self) -> ItemInfo:
        return ItemInfo(name=self.name, price=self.price, deleted=False)  # False - просто заглушка


# contracts for carts
class CartResponse(BaseModel):
    id: int
    items: list[CartItem | None] = []
    price: Annotated[float, Field(ge=0.0)] = 0.0

    @staticmethod
    def from_cart(model: Cart) -> CartResponse:
        return CartResponse(
            id=model.id,
            items=model.info.items,
            price=model.info.price
        )
