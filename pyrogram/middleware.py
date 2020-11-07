from typing import Any, Callable, Coroutine, TypeVar

# import pyrogram

# UpdateType = TypeVar('UpdateType', bound=pyrogram.types.Update)
# ClientType = TypeVar('ClientType', bound=pyrogram.Client)

CallNextMiddlewareCallback = Callable[[Any, Any], Coroutine[Any, Any, Any]]
Middleware = Callable[[Any, Any, CallNextMiddlewareCallback], Coroutine[Any, Any, Any]]
