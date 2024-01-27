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

from typing import Tuple


class DataCenter:
    TEST = {
        1: "149.154.175.10",
        2: "149.154.167.40",
        3: "149.154.175.117",
    }

    PROD = {
        1: "149.154.175.53",
        2: "149.154.167.51",
        3: "149.154.175.100",
        4: "149.154.167.91",
        5: "91.108.56.130",
        203: "91.105.192.100"
    }

    PROD_MEDIA = {
        2: "149.154.167.151",
        4: "149.154.164.250"
    }

    TEST_IPV6 = {
        1: "2001:b28:f23d:f001::e",
        2: "2001:67c:4e8:f002::e",
        3: "2001:b28:f23d:f003::e",
    }

    PROD_IPV6 = {
        1: "2001:b28:f23d:f001::a",
        2: "2001:67c:4e8:f002::a",
        3: "2001:b28:f23d:f003::a",
        4: "2001:67c:4e8:f004::a",
        5: "2001:b28:f23f:f005::a",
        203: "2a0a:f280:0203:000a:5000:0000:0000:0100"
    }

    PROD_IPV6_MEDIA = {
        2: "2001:067c:04e8:f002:0000:0000:0000:000b",
        4: "2001:067c:04e8:f004:0000:0000:0000:000b"
    }

    def __new__(cls, dc_id: int, test_mode: bool, ipv6: bool, media: bool) -> Tuple[str, int]:
        if test_mode:
            if ipv6:
                ip = cls.TEST_IPV6[dc_id]
            else:
                ip = cls.TEST[dc_id]

            return ip, 80
        else:
            if ipv6:
                if media:
                    ip = cls.PROD_IPV6_MEDIA.get(dc_id, cls.PROD_IPV6[dc_id])
                else:
                    ip = cls.PROD_IPV6[dc_id]
            else:
                if media:
                    ip = cls.PROD_MEDIA.get(dc_id, cls.PROD[dc_id])
                else:
                    ip = cls.PROD[dc_id]

            return ip, 443
