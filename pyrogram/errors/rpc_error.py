#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import re
from datetime import datetime
from importlib import import_module
from typing import Type, Union

from pyrogram import raw
from pyrogram.raw.core import TLObject
from .exceptions.all import exceptions


class RPCError(Exception):
    ID = None
    CODE = None
    NAME = None
    MESSAGE = "{x}"

    def __init__(
        self,
        x: Union[int, str, raw.types.RpcError] = None,
        rpc_name: str = None,
        is_unknown: bool = False,
        is_signed: bool = False
    ):
        super().__init__("Telegram says: [{}{} {}] - {} {}".format(
            "-" if is_signed else "",
            self.CODE,
            self.ID or self.NAME,
            self.MESSAGE.format(x=x),
            f'(caused by "{rpc_name}")' if rpc_name else ""
        ))

        try:
            self.x = int(x)
        except (ValueError, TypeError):
            self.x = x

        if is_unknown:
            with open("unknown_errors.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()}\t{x}\t{rpc_name}\n")

    @staticmethod
    def raise_it(rpc_error: "raw.types.RpcError", rpc_type: Type[TLObject]):
        error_code = rpc_error.error_code
        is_signed = error_code < 0
        error_message = rpc_error.error_message
        rpc_name = ".".join(rpc_type.QUALNAME.split(".")[1:])

        if is_signed:
            error_code = -error_code

        if error_code not in exceptions:
            raise UnknownError(
                x=f"[{error_code} {error_message}]",
                rpc_name=rpc_name,
                is_unknown=True,
                is_signed=is_signed
            )

        error_id = re.sub(r"_\d+", "_X", error_message)

        if error_id not in exceptions[error_code]:
            raise getattr(
                import_module("pyrogram.errors"),
                exceptions[error_code]["_"]
            )(x=f"[{error_code} {error_message}]",
              rpc_name=rpc_name,
              is_unknown=True,
              is_signed=is_signed)

        x = re.search(r"_(\d+)", error_message)
        x = x.group(1) if x is not None else x

        raise getattr(
            import_module("pyrogram.errors"),
            exceptions[error_code][error_id]
        )(x=x,
          rpc_name=rpc_name,
          is_unknown=False,
          is_signed=is_signed)


class UnknownError(RPCError):
    CODE = 520
    """:obj:`int`: Error code"""
    NAME = "Unknown error"
