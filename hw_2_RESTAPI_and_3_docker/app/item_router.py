from fastapi import APIRouter, HTTPException, Query, Response, Path
from pydantic import NonNegativeInt, PositiveInt
from typing import List

from typing import Annotated
from http import HTTPStatus

from .contracts import ItemResponse, ItemRequest, PatchItemRequest
from hw_2_RESTAPI_and_3_docker.store import queries

item_router = APIRouter(prefix="/item")


@item_router.post('/',
                  status_code=HTTPStatus.CREATED)
async def post_item(request: ItemRequest, response: Response) -> ItemResponse:
    item = queries.add_item(request.to_item_info())

    response.headers['location'] = f"items/{item.id}"

    return ItemResponse.from_item(item)


@item_router.get('/{id}',
                 responses={
                     HTTPStatus.OK: {
                         "description": "Successfully returned requested item",
                     },
                     HTTPStatus.NOT_FOUND: {
                         "description": "Failed to return requested item as one was not found",
                     },
                 },
)
async def get_item(id: Annotated[int, Path()]) -> ItemResponse:
    item = queries.get_item(id)
    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Item with id {id} does not exist')

    return ItemResponse.from_item(item)


@item_router.get('/')
async def get_list_items(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[float | None, Query(ge=0.)] = None,
        max_price: Annotated[float | None, Query(ge=0.)] = None,
        show_deleted: Annotated[bool, Query()] = False,
) -> List[ItemResponse]:
    return [ItemResponse.from_item(item) for item in queries.get_items(offset=offset, limit=limit, min_price=min_price,
                                                                       max_price=max_price, show_deleted=show_deleted)]


@item_router.put('/{id}')
async def put_item(id: Annotated[int, Path()], request: ItemRequest) -> ItemResponse:
    item = queries.put_item(id=id, new_item=request.to_item_info())
    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED,
                            detail=f'Item with id {id} does not exist or insufficient data')
    return ItemResponse.from_item(item)


@item_router.patch('/{id}')
async def patch_item(id: Annotated[int, Path()], request: PatchItemRequest) -> ItemResponse:
    info = queries.patch_item(id=id, new_item=request.to_item_info())
    if info is None:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED,
                            detail=f'Item with id {id} does not exist or insufficient data')
    return ItemResponse.from_item(info)


@item_router.delete('/{id}')
async def delete_item(id: int) -> None:
    queries.delete_item(id=id)

