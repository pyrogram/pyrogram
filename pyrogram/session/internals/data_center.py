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

    TEST_IPV6 = {
        1: "2001:0b28:f23d:f001:0000:0000:0000:000e",
        2: "2001:067c:04e8:f002:0000:0000:0000:000e",
        3: "2001:0b28:f23d:f003:0000:0000:0000:000e",
        121: "2a03:b0c0:0003:00d0:0000:0000:0114:d001"
    }

    PROD_IPV6 = {
        1: "2001:0b28:f23d:f001:0000:0000:0000:000a",
        2: "2001:067c:04e8:f002:0000:0000:0000:000a",
        3: "2001:0b28:f23d:f003:0000:0000:0000:000a",
        4: "2001:067c:04e8:f004:0000:0000:0000:000a",
        5: "2001:0b28:f23f:f005:0000:0000:0000:000a",
        121: "2a03:b0c0:0003:00d0:0000:0000:0114:d001"
    }

    def __new__(cls, dc_id: int, test_mode: bool, ipv6: bool):
        if ipv6:
            return (cls.TEST_IPV6[dc_id], 80) if test_mode else (cls.PROD_IPV6[dc_id], 443)
        else:
            return (cls.TEST[dc_id], 80) if test_mode else (cls.PROD[dc_id], 443)
