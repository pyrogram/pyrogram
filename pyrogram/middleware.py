from typing import Any, Callable, Coroutine, TypeVar

import pyrogram

UpdateType = TypeVar('UpdateType', bound=pyrogram.types.Update)
ClientType = TypeVar('ClientType', bound=pyrogram.Client)

CallNextMiddlewareCallback = Callable[[ClientType, UpdateType], Coroutine[Any]]
Middleware = Callable[[ClientType, UpdateType, CallNextMiddlewareCallback], Coroutine[Any]]
