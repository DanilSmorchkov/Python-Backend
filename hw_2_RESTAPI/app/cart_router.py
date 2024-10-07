from fastapi import APIRouter, Response, Query, HTTPException, Path
from http import HTTPStatus
from pydantic import NonNegativeInt, PositiveInt
from typing import Annotated, List

from hw_2_RESTAPI.store import queries
from .contracts import CartResponse

cart_router = APIRouter(prefix='/cart')


@cart_router.post('/',
                  status_code=HTTPStatus.CREATED,)
async def create_cart(response: Response):
    cart = queries.add_cart()

    response.headers['location'] = f'/cart/{cart.id}'

    return CartResponse.from_cart(cart)


@cart_router.post('/{id}/add/{item_id}',
                  status_code=HTTPStatus.CREATED)
async def add_item_to_cart(id: Annotated[int, Path()], item_id: Annotated[int, Path()]):
    response = queries.add_item_to_cart(id, item_id)
    if response is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Item does not exist')
    elif response is False:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Cart does not exist')
    else:
        return Response(status_code=HTTPStatus.OK,
                        content='Item has been added to cart',
                        )


@cart_router.get('/{id}')
async def get_cart(id: Annotated[int, Path()]) -> CartResponse:
    cart = queries.get_cart(id)
    if cart is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Cart not found')
    return CartResponse.from_cart(cart)


@cart_router.get('/')
async def get_list_carts(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[float | None, Query(ge=0.)] = None,
        max_price: Annotated[float | None, Query(ge=0.)] = None,
        min_quantity: Annotated[NonNegativeInt | None, Query()] = None,
        max_quantity: Annotated[NonNegativeInt | None, Query()] = None,
) -> List[CartResponse]:
    return [CartResponse.from_cart(cart) for cart in queries.get_carts(
        offset=offset,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
    )]