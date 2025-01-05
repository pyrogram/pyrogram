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

import pyrogram


class RemoveErrorHandler:
    def remove_error_handler(
        self: "pyrogram.Client",
        error: "Exception | tuple[Exception]" = Exception
    ):
        """Remove a previously-registered error handler. (using exception classes)

        Parameters:
            error (``Exception``):
                The error(s) for handlers to be removed.
        """
        for handler in self.dispatcher.error_handlers:
            if handler.check_remove(error):
                self.dispatcher.error_handlers.remove(handler)
