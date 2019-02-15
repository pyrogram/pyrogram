import hashlib
from random import randint
from typing import Union

import pyrogram
from pyrogram.api import types, functions
from tgvoip import CallState
from tgvoip.utils import i2b, b2i, calc_fingerprint

from . import BaseCall


class OutgoingCall(BaseCall):
    outgoing = True

    def __init__(self,
                 client: "pyrogram.client.ext.BaseClient",
                 user_id: Union[int, str]):
        super(OutgoingCall, self).__init__(client)
        self.update_state(CallState.REQUESTING)
        self.peer = self._client.resolve_peer(user_id)
        self.a = randint(2, self.dhc.p)
        self.g_a = pow(self.dhc.g, self.a, self.dhc.p)
        self.check_g(self.g_a, self.dhc.p)
        self.g_a_hash = hashlib.sha256(i2b(self.g_a)).digest()
        self.call = self._client.send(functions.phone.RequestCall(
            user_id=self.peer,
            random_id=randint(0, 0x7fffffff - 1),
            g_a_hash=self.g_a_hash,
            protocol=self.protocol,
        )).phone_call
        self.update_state(CallState.WAITING)

        # self.call_accepted_handlers = []

    def _process_update(self, client, call) -> None:
        super(OutgoingCall, self)._process_update(client, call)
        if isinstance(call, types.PhoneCallAccepted) and not self.auth_key:
            self.call_accepted()
            raise pyrogram.StopPropagation
        raise pyrogram.ContinuePropagation

    def call_accepted(self) -> None:
        # for handler in self.call_accepted_handlers:
        #     callable(handler) and handler(self)

        self.update_state(CallState.EXCHANGING_KEYS)
        self.g_b = b2i(self.call.g_b)
        self.check_g(self.g_b, self.dhc.p)
        self.auth_key = pow(self.g_b, self.a, self.dhc.p)
        self.key_fingerprint = calc_fingerprint(self.auth_key_bytes)
        self.call = self._client.send(functions.phone.ConfirmCall(
            key_fingerprint=self.key_fingerprint,
            peer=types.InputPhoneCall(self.call.id, self.call.access_hash),
            g_a=i2b(self.g_a),
            protocol=self.protocol,
        )).phone_call
        self._initiate_encrypted_call()
