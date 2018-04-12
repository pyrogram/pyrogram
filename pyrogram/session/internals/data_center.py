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


class DataCenter:
    TEST = {
        1: "149.154.175.10",
        2: "149.154.167.40",
        3: "149.154.175.117",
        121: "95.213.217.195"
    }

    PROD = {
        1: "149.154.175.50",
        2: "149.154.167.51",
        3: "149.154.175.100",
        4: "149.154.167.91",
        5: "91.108.56.149",
        121: "95.213.217.195"
    }

    def __new__(cls, dc_id: int, test_mode: bool):
        return (cls.TEST[dc_id], 80) if test_mode else (cls.PROD[dc_id], 443)
