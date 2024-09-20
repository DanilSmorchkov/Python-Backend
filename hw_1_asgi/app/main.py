from errors import NotFound
from typing import Any, Callable, Awaitable
from routes import handle_mean, handle_factorial, handle_fibonacci, send_response


async def app(scope: dict[str, Any],
              receive: Callable[[], Awaitable[dict[str, Any]]],
              send: Callable[[dict[str, Any]], Awaitable[None]]):

    try:
        if scope['type'] == 'http':
            method = scope['method']
            path = scope['path']
            if method == 'GET':
                if path == '/factorial':
                    await handle_factorial(scope=scope, receive=receive, send=send)
                elif path.startswith('/fibonacci'):
                    await handle_fibonacci(scope=scope, receive=receive, send=send)
                elif path == '/mean':
                    await handle_mean(scope=scope, receive=receive, send=send)
                else:
                    raise NotFound('Not Found: no such request exists')
            else:
                raise NotFound('Not Found: method is not GET')

        else:
            raise NotFound('Not Found: only HTTP is supported')

    except NotFound as exc:
        data = {'error': exc.detail}
        await send_response(send=send, data=data, status=exc.status_code)
