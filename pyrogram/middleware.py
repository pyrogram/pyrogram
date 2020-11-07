from typing import Any, Callable, Coroutine, TypeVar

from pyrogram import Client
from pyrogram.types import Update

UpdateType = TypeVar('UpdateType', bound=Update)
CallNextMiddlewareCallback = Callable[[Client, UpdateType], Coroutine[Any]]
Middleware = Callable[[Client, UpdateType, CallNextMiddlewareCallback], Coroutine[Any]]
