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

import logging
import time
from hashlib import sha1
from io import BytesIO
from os import urandom

from pyrogram.api import functions, types
from pyrogram.api.core import Object, Long, Int
from pyrogram.connection import Connection
from pyrogram.crypto import AES, RSA, Prime
from .internals import MsgId, DataCenter

log = logging.getLogger(__name__)


class Auth:
    MAX_RETRIES = 5

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

    def __init__(self, dc_id: int, test_mode: bool, proxy: dict):
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.proxy = proxy

        self.connection = None

    @staticmethod
    def pack(data: Object) -> bytes:
        return (
            bytes(8)
            + Long(MsgId())
            + Int(len(data.write()))
            + data.write()
        )

    @staticmethod
    def unpack(b: BytesIO):
        b.seek(20)  # Skip auth_key_id (8), message_id (8) and message_length (4)
        return Object.read(b)

    def send(self, data: Object):
        data = self.pack(data)
        self.connection.send(data)
        response = BytesIO(self.connection.recv())

        return self.unpack(response)

    def create(self):
        """
        https://core.telegram.org/mtproto/auth_key
        https://core.telegram.org/mtproto/samples-auth_key
        """
        retries_left = self.MAX_RETRIES

        # The server may close the connection at any time, causing the auth key creation to fail.
        # If that happens, just try again up to MAX_RETRIES times.
        while True:
            self.connection = Connection(DataCenter(self.dc_id, self.test_mode), self.proxy)

            try:
                log.info("Start creating a new auth key on DC{}".format(self.dc_id))

                self.connection.connect()

                # Step 1; Step 2
                nonce = int.from_bytes(urandom(16), "little", signed=True)
                log.debug("Send req_pq: {}".format(nonce))
                res_pq = self.send(functions.ReqPqMulti(nonce))
                log.debug("Got ResPq: {}".format(res_pq.server_nonce))
                log.debug("Server public key fingerprints: {}".format(res_pq.server_public_key_fingerprints))

                for i in res_pq.server_public_key_fingerprints:
                    if i in RSA.server_public_keys:
                        log.debug("Using fingerprint: {}".format(i))
                        public_key_fingerprint = i
                        break
                    else:
                        log.debug("Fingerprint unknown: {}".format(i))
                else:
                    raise Exception("Public key not found")

                # Step 3
                pq = int.from_bytes(res_pq.pq, "big")
                log.debug("Start PQ factorization: {}".format(pq))
                start = time.time()
                g = Prime.decompose(pq)
                p, q = sorted((g, pq // g))  # p < q
                log.debug("Done PQ factorization ({}s): {} {}".format(round(time.time() - start, 3), p, q))

                # Step 4
                server_nonce = res_pq.server_nonce
                new_nonce = int.from_bytes(urandom(32), "little", signed=True)

                data = types.PQInnerData(
                    res_pq.pq,
                    int.to_bytes(p, 4, "big"),
                    int.to_bytes(q, 4, "big"),
                    nonce,
                    server_nonce,
                    new_nonce,
                ).write()

                sha = sha1(data).digest()
                padding = urandom(- (len(data) + len(sha)) % 255)
                data_with_hash = sha + data + padding
                encrypted_data = RSA.encrypt(data_with_hash, public_key_fingerprint)

                log.debug("Done encrypt data with RSA")

                # Step 5. TODO: Handle "server_DH_params_fail". Code assumes response is ok
                log.debug("Send req_DH_params")
                server_dh_params = self.send(
                    functions.ReqDHParams(
                        nonce,
                        server_nonce,
                        int.to_bytes(p, 4, "big"),
                        int.to_bytes(q, 4, "big"),
                        public_key_fingerprint,
                        encrypted_data
                    )
                )

                encrypted_answer = server_dh_params.encrypted_answer

                server_nonce = int.to_bytes(server_nonce, 16, "little", signed=True)
                new_nonce = int.to_bytes(new_nonce, 32, "little", signed=True)

                tmp_aes_key = (
                    sha1(new_nonce + server_nonce).digest()
                    + sha1(server_nonce + new_nonce).digest()[:12]
                )

                tmp_aes_iv = (
                    sha1(server_nonce + new_nonce).digest()[12:]
                    + sha1(new_nonce + new_nonce).digest() + new_nonce[:4]
                )

                server_nonce = int.from_bytes(server_nonce, "little", signed=True)

                answer_with_hash = AES.ige256_decrypt(encrypted_answer, tmp_aes_key, tmp_aes_iv)
                answer = answer_with_hash[20:]

                server_dh_inner_data = Object.read(BytesIO(answer))

                log.debug("Done decrypting answer")

                dh_prime = int.from_bytes(server_dh_inner_data.dh_prime, "big")
                delta_time = server_dh_inner_data.server_time - time.time()

                log.debug("Delta time: {}".format(round(delta_time, 3)))

                # Step 6
                g = server_dh_inner_data.g
                b = int.from_bytes(urandom(256), "big")
                g_b = int.to_bytes(pow(g, b, dh_prime), 256, "big")

                retry_id = 0

                data = types.ClientDHInnerData(
                    nonce,
                    server_nonce,
                    retry_id,
                    g_b
                ).write()

                sha = sha1(data).digest()
                padding = urandom(- (len(data) + len(sha)) % 16)
                data_with_hash = sha + data + padding
                encrypted_data = AES.ige256_encrypt(data_with_hash, tmp_aes_key, tmp_aes_iv)

                log.debug("Send set_client_DH_params")
                set_client_dh_params_answer = self.send(
                    functions.SetClientDHParams(
                        nonce,
                        server_nonce,
                        encrypted_data
                    )
                )

                # TODO: Handle "auth_key_aux_hash" if the previous step fails

                # Step 7; Step 8
                g_a = int.from_bytes(server_dh_inner_data.g_a, "big")
                auth_key = int.to_bytes(pow(g_a, b, dh_prime), 256, "big")
                server_nonce = int.to_bytes(server_nonce, 16, "little", signed=True)

                # TODO: Handle errors

                #######################
                # Security checks
                #######################

                assert dh_prime == self.CURRENT_DH_PRIME
                log.debug("DH parameters check: OK")

                # https://core.telegram.org/mtproto/security_guidelines#g-a-and-g-b-validation
                g_b = int.from_bytes(g_b, "big")
                assert 1 < g < dh_prime - 1
                assert 1 < g_a < dh_prime - 1
                assert 1 < g_b < dh_prime - 1
                assert 2 ** (2048 - 64) < g_a < dh_prime - 2 ** (2048 - 64)
                assert 2 ** (2048 - 64) < g_b < dh_prime - 2 ** (2048 - 64)
                log.debug("g_a and g_b validation: OK")

                # https://core.telegram.org/mtproto/security_guidelines#checking-sha1-hash-values
                answer = server_dh_inner_data.write()  # Call .write() to remove padding
                assert answer_with_hash[:20] == sha1(answer).digest()
                log.debug("SHA1 hash values check: OK")

                # https://core.telegram.org/mtproto/security_guidelines#checking-nonce-server-nonce-and-new-nonce-fields
                # 1st message
                assert nonce == res_pq.nonce
                # 2nd message
                server_nonce = int.from_bytes(server_nonce, "little", signed=True)
                assert nonce == server_dh_params.nonce
                assert server_nonce == server_dh_params.server_nonce
                # 3rd message
                assert nonce == set_client_dh_params_answer.nonce
                assert server_nonce == set_client_dh_params_answer.server_nonce
                server_nonce = int.to_bytes(server_nonce, 16, "little", signed=True)
                log.debug("Nonce fields check: OK")

                # Step 9
                server_salt = AES.xor(new_nonce[:8], server_nonce[:8])

                log.debug("Server salt: {}".format(int.from_bytes(server_salt, "little")))

                log.info(
                    "Done auth key exchange: {}".format(
                        set_client_dh_params_answer.__class__.__name__
                    )
                )
            except Exception as e:
                if retries_left:
                    retries_left -= 1
                else:
                    raise e

                time.sleep(1)
                continue
            else:
                return auth_key
            finally:
                self.connection.close()
