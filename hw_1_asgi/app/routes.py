from errors import BadRequest, UnProcessable, HTTPException
from typing import Any, Callable, Awaitable
from urllib.parse import parse_qs
import json


async def handle_factorial(scope: dict[str, Any],
                           receive: Callable[[], Awaitable[dict[str, Any]]],
                           send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
    try:
        query = parse_qs(scope['query_string'].decode())
        n_str = query.get('n', None)
        if n_str is None or not n_str[0].strip('-').isdigit():
            raise UnProcessable('Unprocessable Entity: the parameter must be called n and be a positive integer')

        n = int(n_str[0])
        if n < 0:
            raise BadRequest('Bad Request: n must be a positive integer')

        def factorial(n: int) -> int:
            ans = 1
            for i in range(1, n+1):
                ans *= i
            return ans

        answer = {'result': factorial(n)}
        await send_response(send=send, data=answer, status=200)

    except HTTPException as exc:
        data = {'error': exc.detail}
        await send_response(send=send, status=exc.status_code, data=data)


async def handle_fibonacci(scope: dict[str, Any],
                           receive: Callable[[], Awaitable[dict[str, Any]]],
                           send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
    try:
        n_str = scope['path'].strip('/').split('/')[-1]
        if not n_str.strip('-').isdigit():
            raise UnProcessable('Unprocessable Entity: the parameter must be a positive integer')
        n = int(n_str)
        if n < 0:
            raise BadRequest('Bad Request: n must be a positive integer')

        def fibonacci(n: int) -> int:
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return a

        answer = {'result': fibonacci(n)}
        await send_response(send=send, data=answer, status=200)

    except HTTPException as exc:
        data = {'error': exc.detail}
        await send_response(send=send, data=data, status=exc.status_code)


async def handle_mean(scope: dict[str, Any],
                      receive: Callable[[], Awaitable[dict[str, Any]]],
                      send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
    body = await read_body(receive)
    try:
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise UnProcessable('Unprocessable Entity: invalid JSON')
        if not isinstance(data, list):
            raise UnProcessable('Unprocessable Entity: the parameter must be a list of floats')
        if len(data) == 0:
            raise BadRequest('Bad Request: an empty list')
        if not all(isinstance(x, (float, int)) for x in data):
            raise UnProcessable('Unprocessable Entity: the parameter must be a list of floats')

        answer = {'result': sum(data) / len(data)}
        await send_response(send=send, data=answer, status=200)

    except HTTPException as exc:
        data = {'error': exc.detail}
        await send_response(send=send, data=data, status=exc.status_code)


async def read_body(receive: Callable[[], Awaitable[dict[str, Any]]]) -> str:
    body = b''
    more_body = True
    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body.decode()


async def send_response(send: Callable[[dict[str, Any]],Awaitable[None]],
                        data: dict[str, Any],
                        status: int) -> None:
    body = json.dumps(data).encode()
    headers = [(b'content-type', b'application/json')]

    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': headers
    })

    await send({
        'type': 'http.response.body',
        'body': body,
        'more_body': False
    })
