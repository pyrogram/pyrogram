from __future__ import annotations

from typing import (
    Any,
    Callable,
    Coroutine,
)

CallNextMiddlewareCallable = Callable[['pyrogram.Client', 'pyrogram.types.Update'], Coroutine[Any, Any, Any]]
Middleware = Callable[['pyrogram.Client', 'pyrogram.types.Update', CallNextMiddlewareCallable], Coroutine[Any, Any, Any]]
