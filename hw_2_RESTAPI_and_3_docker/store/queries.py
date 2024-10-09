from typing import Iterable
from .models import Item, Cart, ItemInfo, CartItem, CartInfo


_item_data = dict[int, ItemInfo]()
_cart_data = dict[int, CartInfo]()


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_item_id_generator = iter(int_id_generator())
_cart_id_generator = iter(int_id_generator())


# queries for items
def add_item(info: ItemInfo) -> Item:
    _id = next(_item_id_generator)
    _item_data[_id] = info
    return Item(id=_id, info=info)


def get_item(id: int) -> Item | None:
    if id not in _item_data or _item_data[id].deleted is True:
        return None
    return Item(id=id, info=_item_data[id])


def get_items(offset: int, limit: int, min_price: float | None, max_price: float | None,
              show_deleted: bool) -> Iterable[Item]:
    curr = 0
    for id, item_info in _item_data.items():
        if offset <= curr < offset + limit:
            if min_price is None or item_info.price <= min_price:
                if max_price is None or item_info.price >= max_price:
                    if item_info.deleted and show_deleted:
                        yield Item(id=id, info=item_info)
        curr += 1


def put_item(id: int, new_item: ItemInfo) -> Item | None:
    if id not in _item_data:
        return None
    if not new_item.price or not new_item.name:
        return None

    _item_data[id] = new_item
    return Item(id=id, info=new_item)


def patch_item(id: int, new_item: ItemInfo) -> Item | None:
    if id not in _item_data or _item_data[id].deleted is True:
        return None

    if new_item.price:
        _item_data[id].price = new_item.price

    if new_item.name:
        _item_data[id].name = new_item.name

    return Item(id=id, info=_item_data[id])


def delete_item(id: int) -> None:
    if id not in _item_data:
        return None
    _item_data[id].deleted = True


# queries for carts
def add_cart() -> Cart:
    id = next(_cart_id_generator)
    cart = Cart(id=id, info=CartInfo())
    _cart_data[id] = CartInfo()
    return cart


def add_item_to_cart(id: int, item_id: int) -> bool | None:
    if id not in _cart_data:
        return False
    if item_id not in _item_data and _item_data[item_id].deleted:
        return None
    item = _item_data[item_id]
    cart_info = _cart_data[id]
    cart_info.price += item.price
    for cart_item in cart_info.items:
        if cart_item.id == item_id:
            cart_item.quantity += 1
            break
    else:
        cart_item = CartItem(id=item_id, name=item.name, quantity=1, available=True)
        cart_info.items.append(cart_item)
        return True


def check_cart(id: int) -> CartInfo:
    cart_info = _cart_data[id]
    total_price = 0.
    checked_items = []
    for cart_item in cart_info.items:
        item = get_item(cart_item.id)
        if item:
            total_price += item.info.price * cart_item.quantity
            cart_item.available = True
            cart_item.name = item.info.name
        else:
            cart_item.available = False

        checked_items.append(cart_item)

    cart_info.price = total_price
    cart_info.items = checked_items
    return cart_info


def get_cart(id: int) -> Cart | None:
    if id not in _cart_data:
        return None
    cart_info = check_cart(id)
    return Cart(id=id, info=cart_info)


def get_carts(offset: int, limit: int, min_price: float | None, max_price: float | None,
              min_quantity: int, max_quantity: int) -> Iterable[Cart]:
    curr = 0
    for cart_info in _cart_data.values():
        if offset <= curr < offset + limit:
            if min_price is None or cart_info.price >= min_price:
                if max_price is None or cart_info.price <= max_price:
                    total_quantity = sum(item.quantity for item in cart_info.items)
                    if min_quantity is None or total_quantity >= min_quantity:
                        if max_quantity is None or total_quantity <= max_quantity:
                            cart_info = check_cart(curr)
                            yield Cart(id=curr, info=cart_info)
        curr += 1
