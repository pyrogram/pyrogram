#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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


class KeyboardButtonPollType:
    """This object represents type of a poll,
    which is allowed to be created and sent when the corresponding button is pressed.
    
    Parameters:
        type (``str``, *optional*):
            If quiz is passed, the user will be allowed to create only polls in the quiz mode.
            If regular is passed, only regular polls will be allowed.
            Otherwise, the user will be allowed to create a poll of any type.
    """
    def __init__(
        self,
        type: str = ""
    ):
        self.type = type
