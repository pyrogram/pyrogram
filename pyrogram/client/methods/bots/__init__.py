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

from .answer_callback_query import AnswerCallbackQuery
from .get_inline_bot_results import GetInlineBotResults
from .request_callback_answer import RequestCallbackAnswer
from .send_inline_bot_result import SendInlineBotResult


class Bots(
    AnswerCallbackQuery,
    GetInlineBotResults,
    RequestCallbackAnswer,
    SendInlineBotResult
):
    pass
