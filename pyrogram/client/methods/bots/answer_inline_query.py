# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient


class AnswerInlineQuery(BaseClient):
    def answer_inline_query(
        self,
        inline_query_id: str,
        results: list,
        cache_time: int = 300,
        is_personal: bool = None,
        next_offset: str = "",
        switch_pm_text: str = "",
        switch_pm_parameter: str = ""
    ):
        # TODO: Docs
        return self.send(
            functions.messages.SetInlineBotResults(
                query_id=int(inline_query_id),
                results=[r.write() for r in results],
                cache_time=cache_time,
                gallery=None,
                private=is_personal or None,
                next_offset=next_offset or None,
                switch_pm=types.InlineBotSwitchPM(
                    text=switch_pm_text,
                    start_param=switch_pm_parameter
                ) if switch_pm_text else None
            )
        )
