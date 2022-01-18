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

import logging

log = logging.getLogger(__name__)

try:
    import tgcrypto

    log.info("Using TgCrypto")


    def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return tgcrypto.ige256_encrypt(data, key, iv)


    def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return tgcrypto.ige256_decrypt(data, key, iv)


    def ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
        return tgcrypto.ctr256_encrypt(data, key, iv, state or bytearray(1))


    def ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
        return tgcrypto.ctr256_decrypt(data, key, iv, state or bytearray(1))


    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )
except ImportError:
    import pyaes

    log.warning(
        "TgCrypto is missing! "
        "Pyrogram will work the same, but at a much slower speed. "
        "More info: https://docs.pyrogram.org/topics/tgcrypto"
    )


    def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return ige(data, key, iv, True)


    def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return ige(data, key, iv, False)


    def ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
        return ctr(data, key, iv, state or bytearray(1))


    def ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
        return ctr(data, key, iv, state or bytearray(1))


    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )


    def ige(data: bytes, key: bytes, iv: bytes, encrypt: bool) -> bytes:
        cipher = pyaes.AES(key)

        iv_1 = iv[:16]
        iv_2 = iv[16:]

        data = [data[i: i + 16] for i in range(0, len(data), 16)]

        if encrypt:
            for i, chunk in enumerate(data):
                iv_1 = data[i] = xor(cipher.encrypt(xor(chunk, iv_1)), iv_2)
                iv_2 = chunk
        else:
            for i, chunk in enumerate(data):
                iv_2 = data[i] = xor(cipher.decrypt(xor(chunk, iv_2)), iv_1)
                iv_1 = chunk

        return b"".join(data)


    def ctr(data: bytes, key: bytes, iv: bytearray, state: bytearray) -> bytes:
        cipher = pyaes.AES(key)

        out = bytearray(data)
        chunk = cipher.encrypt(iv)

        for i in range(0, len(data), 16):
            for j in range(0, min(len(data) - i, 16)):
                out[i + j] ^= chunk[state[0]]

                state[0] += 1

                if state[0] >= 16:
                    state[0] = 0

                if state[0] == 0:
                    for k in range(15, -1, -1):
                        try:
                            iv[k] += 1
                            break
                        except ValueError:
                            iv[k] = 0

                    chunk = cipher.encrypt(iv)

        return out
