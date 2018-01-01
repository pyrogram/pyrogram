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

from random import randint


class Prime:
    # Recursive variant
    # @classmethod
    # def gcd(cls, a: int, b: int) -> int:
    #     return cls.gcd(b, a % b) if b else a

    @staticmethod
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b

        return a

    @classmethod
    def decompose(cls, pq: int) -> int:
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

                g = cls.gcd(q, pq)
                k += m

            r *= 2

        if g == pq:
            while True:
                ys = (pow(ys, 2, pq) + c) % pq
                g = cls.gcd(abs(x - ys), pq)

                if g > 1:
                    break

        return g
