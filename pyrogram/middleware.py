from typing import Any, Callable, Coroutine

# For better IDE typing support, but have circular imports error
# import pyrogram
#
# ClientType = TypeVar('ClientType', bound=pyrogram.Client)
# UpdateType = TypeVar('UpdateType', bound=pyrogram.types.Update)
# CallNextMiddlewareCallable = Callable[[ClientType, UpdateType], Coroutine[Any, Any, Any]]
# Middleware = Callable[[ClientType, UpdateType, CallNextMiddlewareCallable], Coroutine[Any, Any, Any]]

CallNextMiddlewareCallable = Callable[[Any, Any], Coroutine[Any, Any, Any]]
Middleware = Callable[[Any, Any, CallNextMiddlewareCallable], Coroutine[Any, Any, Any]]
