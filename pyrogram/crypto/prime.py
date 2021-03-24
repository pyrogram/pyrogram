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

from random import randint

CURRENT_DH_PRIME = int(
    "C71CAEB9C6B1C9048E6C522F70F13F73980D40238E3E21C14934D037563D930F"
    "48198A0AA7C14058229493D22530F4DBFA336F6E0AC925139543AED44CCE7C37"
    "20FD51F69458705AC68CD4FE6B6B13ABDC9746512969328454F18FAF8C595F64"
    "2477FE96BB2A941D5BCD1D4AC8CC49880708FA9B378E3C4F3A9060BEE67CF9A4"
    "A4A695811051907E162753B56B0F6B410DBA74D8A84B2A14B3144E0EF1284754"
    "FD17ED950D5965B4B9DD46582DB1178D169C6BC465B0D6FF9CA3928FEF5B9AE4"
    "E418FC15E83EBEA0F87FA9FF5EED70050DED2849F47BF959D956850CE929851F"
    "0D8115F635B105EE2E4E15D04B2454BF6F4FADF034B10403119CD8E3B92FCC5B",
    16
)


# Recursive variant
# def gcd(cls, a: int, b: int) -> int:
#     return cls.gcd(b, a % b) if b else a

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b

    return a


def decompose(pq: int) -> int:
    # https://comeoncodeon.wordpress.com/2010/09/18/pollard-rho-brent-integer-factorization/
    if pq % 2 == 0:
        return 2

    y, c, m = randint(1, pq - 1), randint(1, pq - 1), randint(1, pq - 1)
    g = r = q = 1
    x = ys = 0

    while g == 1:
        x = y

        for i in range(r):
            y = (pow(y, 2, pq) + c) % pq

        k = 0

        while k < r and g == 1:
            ys = y

            for i in range(min(m, r - k)):
                y = (pow(y, 2, pq) + c) % pq
                q = q * (abs(x - y)) % pq

            g = gcd(q, pq)
            k += m

        r *= 2

    if g == pq:
        while True:
            ys = (pow(ys, 2, pq) + c) % pq
            g = gcd(abs(x - ys), pq)

            if g > 1:
                break

    return g
