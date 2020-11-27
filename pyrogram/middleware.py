from typing import Any, Callable, Coroutine, TypeVar

from .scaffold import Scaffold
from .types import Update

# Unable to use due to circular imports error
# ClientType = TypeVar('ClientType', bound=Client)
ScaffoldType = TypeVar('ScaffoldType', bound=Scaffold)
UpdateType = TypeVar('UpdateType', bound=Update)
CallNextMiddlewareCallable = Callable[[ScaffoldType, UpdateType], Coroutine[Any, Any, Any]]
Middleware = Callable[[ScaffoldType, UpdateType, CallNextMiddlewareCallable], Coroutine[Any, Any, Any]]
