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

from hashlib import sha256, pbkdf2_hmac
import os

from pyrogram.api import functions, types
from ...ext import BaseClient


def compute_hash(algo: types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow, password: str):
    hash1 = sha256(algo.salt1 + password.encode() + algo.salt1).digest()
    hash2 = sha256(algo.salt2 + hash1 + algo.salt2).digest()
    hash3 = pbkdf2_hmac("sha512", hash2, algo.salt1, 100000)

    return sha256(algo.salt2 + hash3 + algo.salt2).digest()


def btoi(b: bytes):
    return int.from_bytes(b, "big")


def itob(i: int):
    return i.to_bytes(256, "big")


class EnableCloudPassword(BaseClient):
    def enable_cloud_password(self, password: str, hint: str = "", email: str = ""):
        """Use this method to enable the Two-Step Verification security feature (Cloud Password) on your account.

        This password will be asked when you log in on a new device in addition to the SMS code.

        Args:
            password (``str``):
                Your password.

            hint (``str``, *optional*):
                A password hint.

            email (``str``, *optional*):
                Recovery e-mail.

        Returns:
            True on success, False otherwise.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        r = self.send(functions.account.GetPassword())
        print(r)

        algo = r.new_algo

        p_bytes = algo.p
        p = btoi(algo.p)

        g_bytes = itob(algo.g)
        g = algo.g

        B_bytes = r.srp_B or b""
        B = btoi(B_bytes)

        srp_id = r.srp_id or 0

        x_bytes = compute_hash(algo, password)
        x = btoi(x_bytes)

        g_x = pow(g, x, p)

        k_bytes = sha256(p_bytes + g_bytes).digest()
        k = btoi(k_bytes)

        kg_x = (k * g_x) % p

        while True:
            a_bytes = os.urandom(256)
            a = btoi(a_bytes)

            A = pow(g, a, p)
            A_bytes = itob(A)

            u = btoi(sha256(A_bytes + B_bytes).digest())

            if u > 0:
                break

        g_b = (B - kg_x) % p

        ux = u * x
        a_ux = a + ux
        S = pow(g_b, a_ux, p)
        S_bytes = itob(S)

        K_bytes = sha256(S_bytes).digest()
        M1_bytes = sha256(
            b"".join([bytes([int(i) ^ int(j)]) for (i, j) in zip(sha256(p_bytes).digest(), sha256(g_bytes).digest())])
            + sha256(algo.salt1).digest()
            + sha256(algo.salt2).digest()
            + A_bytes
            + B_bytes
            + K_bytes
        ).digest()

        input_check_password = types.InputCheckPasswordSRP(srp_id, A_bytes, M1_bytes)

        r2 = self.send(functions.account.UpdatePasswordSettings(
            input_check_password, types.account.PasswordInputSettings(
                new_algo=algo,
                new_password_hash=b"",
                hint=""
            )
        ))

        print(r2)

        # if isinstance(r, types.account.NoPassword):
        #     salt = r.new_salt + os.urandom(8)
        #     password_hash = sha256(salt + password.encode() + salt).digest()
        #
        #     return self.send(
        #         functions.account.UpdatePasswordSettings(
        #             current_password_hash=salt,
        #             new_settings=types.account.PasswordInputSettings(
        #                 new_salt=salt,
        #                 new_password_hash=password_hash,
        #                 hint=hint,
        #                 email=email
        #             )
        #         )
        #     )
        # else:
        #     return False
