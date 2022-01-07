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

import asyncio
import logging
import time
from hashlib import sha1
from io import BytesIO
from os import urandom

import pyrogram
from pyrogram import raw
from pyrogram.connection import Connection
from pyrogram.crypto import aes, rsa, prime
from pyrogram.errors import SecurityCheckMismatch
from pyrogram.raw.core import TLObject, Long, Int
from .internals import MsgId

log = logging.getLogger(__name__)


class Auth:
    MAX_RETRIES = 5

    def __init__(self, client: "pyrogram.Client", dc_id: int, test_mode: bool):
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.ipv6 = client.ipv6
        self.proxy = client.proxy

        self.connection = None

    @staticmethod
    def pack(data: TLObject) -> bytes:
        return (
            bytes(8)
            + Long(MsgId())
            + Int(len(data.write()))
            + data.write()
        )

    @staticmethod
    def unpack(b: BytesIO):
        b.seek(20)  # Skip auth_key_id (8), message_id (8) and message_length (4)
        return TLObject.read(b)

    async def send(self, data: TLObject):
        data = self.pack(data)
        await self.connection.send(data)
        response = BytesIO(await self.connection.recv())

        return self.unpack(response)

    async def create(self):
        """
        https://core.telegram.org/mtproto/auth_key
        https://core.telegram.org/mtproto/samples-auth_key
        """
        retries_left = self.MAX_RETRIES

        # The server may close the connection at any time, causing the auth key creation to fail.
        # If that happens, just try again up to MAX_RETRIES times.
        while True:
            self.connection = Connection(self.dc_id, self.test_mode, self.ipv6, self.proxy)

            try:
                log.info(f"Start creating a new auth key on DC{self.dc_id}")

                await self.connection.connect()

                # Step 1; Step 2
                nonce = int.from_bytes(urandom(16), "little", signed=True)
                log.debug(f"Send req_pq: {nonce}")
                res_pq = await self.send(raw.functions.ReqPqMulti(nonce=nonce))
                log.debug(f"Got ResPq: {res_pq.server_nonce}")
                log.debug(f"Server public key fingerprints: {res_pq.server_public_key_fingerprints}")

                for i in res_pq.server_public_key_fingerprints:
                    if i in rsa.server_public_keys:
                        log.debug(f"Using fingerprint: {i}")
                        public_key_fingerprint = i
                        break
                    else:
                        log.debug(f"Fingerprint unknown: {i}")
                else:
                    raise Exception("Public key not found")

                # Step 3
                pq = int.from_bytes(res_pq.pq, "big")
                log.debug(f"Start PQ factorization: {pq}")
                start = time.time()
                g = prime.decompose(pq)
                p, q = sorted((g, pq // g))  # p < q
                log.debug(f"Done PQ factorization ({round(time.time() - start, 3)}s): {p} {q}")

                # Step 4
                server_nonce = res_pq.server_nonce
                new_nonce = int.from_bytes(urandom(32), "little", signed=True)

                data = raw.types.PQInnerData(
                    pq=res_pq.pq,
                    p=p.to_bytes(4, "big"),
                    q=q.to_bytes(4, "big"),
                    nonce=nonce,
                    server_nonce=server_nonce,
                    new_nonce=new_nonce,
                ).write()

                sha = sha1(data).digest()
                padding = urandom(- (len(data) + len(sha)) % 255)
                data_with_hash = sha + data + padding
                encrypted_data = rsa.encrypt(data_with_hash, public_key_fingerprint)

                log.debug("Done encrypt data with RSA")

                # Step 5. TODO: Handle "server_DH_params_fail". Code assumes response is ok
                log.debug("Send req_DH_params")
                server_dh_params = await self.send(
                    raw.functions.ReqDHParams(
                        nonce=nonce,
                        server_nonce=server_nonce,
                        p=p.to_bytes(4, "big"),
                        q=q.to_bytes(4, "big"),
                        public_key_fingerprint=public_key_fingerprint,
                        encrypted_data=encrypted_data
                    )
                )

                encrypted_answer = server_dh_params.encrypted_answer

                server_nonce = server_nonce.to_bytes(16, "little", signed=True)
                new_nonce = new_nonce.to_bytes(32, "little", signed=True)

                tmp_aes_key = (
                    sha1(new_nonce + server_nonce).digest()
                    + sha1(server_nonce + new_nonce).digest()[:12]
                )

                tmp_aes_iv = (
                    sha1(server_nonce + new_nonce).digest()[12:]
                    + sha1(new_nonce + new_nonce).digest() + new_nonce[:4]
                )

                server_nonce = int.from_bytes(server_nonce, "little", signed=True)

                answer_with_hash = aes.ige256_decrypt(encrypted_answer, tmp_aes_key, tmp_aes_iv)
                answer = answer_with_hash[20:]

                server_dh_inner_data = TLObject.read(BytesIO(answer))

                log.debug("Done decrypting answer")

                dh_prime = int.from_bytes(server_dh_inner_data.dh_prime, "big")
                delta_time = server_dh_inner_data.server_time - time.time()

                log.debug(f"Delta time: {round(delta_time, 3)}")

                # Step 6
                g = server_dh_inner_data.g
                b = int.from_bytes(urandom(256), "big")
                g_b = pow(g, b, dh_prime).to_bytes(256, "big")

                retry_id = 0

                data = raw.types.ClientDHInnerData(
                    nonce=nonce,
                    server_nonce=server_nonce,
                    retry_id=retry_id,
                    g_b=g_b
                ).write()

                sha = sha1(data).digest()
                padding = urandom(- (len(data) + len(sha)) % 16)
                data_with_hash = sha + data + padding
                encrypted_data = aes.ige256_encrypt(data_with_hash, tmp_aes_key, tmp_aes_iv)

                log.debug("Send set_client_DH_params")
                set_client_dh_params_answer = await self.send(
                    raw.functions.SetClientDHParams(
                        nonce=nonce,
                        server_nonce=server_nonce,
                        encrypted_data=encrypted_data
                    )
                )

                # TODO: Handle "auth_key_aux_hash" if the previous step fails

                # Step 7; Step 8
                g_a = int.from_bytes(server_dh_inner_data.g_a, "big")
                auth_key = pow(g_a, b, dh_prime).to_bytes(256, "big")
                server_nonce = server_nonce.to_bytes(16, "little", signed=True)

                # TODO: Handle errors

                #######################
                # Security checks
                #######################

                SecurityCheckMismatch.check(dh_prime == prime.CURRENT_DH_PRIME)
                log.debug("DH parameters check: OK")

                # https://core.telegram.org/mtproto/security_guidelines#g-a-and-g-b-validation
                g_b = int.from_bytes(g_b, "big")
                SecurityCheckMismatch.check(1 < g < dh_prime - 1)
                SecurityCheckMismatch.check(1 < g_a < dh_prime - 1)
                SecurityCheckMismatch.check(1 < g_b < dh_prime - 1)
                SecurityCheckMismatch.check(2 ** (2048 - 64) < g_a < dh_prime - 2 ** (2048 - 64))
                SecurityCheckMismatch.check(2 ** (2048 - 64) < g_b < dh_prime - 2 ** (2048 - 64))
                log.debug("g_a and g_b validation: OK")

                # https://core.telegram.org/mtproto/security_guidelines#checking-sha1-hash-values
                answer = server_dh_inner_data.write()  # Call .write() to remove padding
                SecurityCheckMismatch.check(answer_with_hash[:20] == sha1(answer).digest())
                log.debug("SHA1 hash values check: OK")

                # https://core.telegram.org/mtproto/security_guidelines#checking-nonce-server-nonce-and-new-nonce-fields
                # 1st message
                SecurityCheckMismatch.check(nonce == res_pq.nonce)
                # 2nd message
                server_nonce = int.from_bytes(server_nonce, "little", signed=True)
                SecurityCheckMismatch.check(nonce == server_dh_params.nonce)
                SecurityCheckMismatch.check(server_nonce == server_dh_params.server_nonce)
                # 3rd message
                SecurityCheckMismatch.check(nonce == set_client_dh_params_answer.nonce)
                SecurityCheckMismatch.check(server_nonce == set_client_dh_params_answer.server_nonce)
                server_nonce = server_nonce.to_bytes(16, "little", signed=True)
                log.debug("Nonce fields check: OK")

                # Step 9
                server_salt = aes.xor(new_nonce[:8], server_nonce[:8])

                log.debug(f"Server salt: {int.from_bytes(server_salt, 'little')}")

                log.info(f"Done auth key exchange: {set_client_dh_params_answer.__class__.__name__}")
            except Exception as e:
                if retries_left:
                    retries_left -= 1
                else:
                    raise e

                await asyncio.sleep(1)
                continue
            else:
                return auth_key
            finally:
                self.connection.close()
