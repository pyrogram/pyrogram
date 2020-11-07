from typing import Any, Callable, Coroutine, TypeVar

from pyrogram import Client
from pyrogram.types import Update

UpdateType = TypeVar('UpdateType', bound=Update)
ClientType = TypeVar('ClientType', bound=Client)

CallNextMiddlewareCallback = Callable[[ClientType, UpdateType], Coroutine[Any]]
Middleware = Callable[[ClientType, UpdateType, CallNextMiddlewareCallback], Coroutine[Any]]
