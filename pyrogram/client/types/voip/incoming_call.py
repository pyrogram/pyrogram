import hashlib
from random import randint

import pyrogram
from pyrogram.api import types, functions, errors
from tgvoip import CallState
from tgvoip.utils import i2b, b2i, calc_fingerprint

from . import BaseCall


class IncomingCall(BaseCall):
    def __init__(self,
                 client: "pyrogram.client.ext.BaseClient",
                 call: types.PhoneCallRequested):
        super(IncomingCall, self).__init__(client)
        self.update_state(CallState.WAITING_INCOMING)
        self.call = call
        self.call_access_hash = call.access_hash

    def _process_update(self, client, call):
        super(IncomingCall, self)._process_update(client, call)
        if isinstance(call, types.PhoneCall) and not self.auth_key:
            self.call_accepted()
            raise pyrogram.StopPropagation
        raise pyrogram.ContinuePropagation

    def accept(self) -> bool:
        self.update_state(CallState.EXCHANGING_KEYS)
        if not self.call:
            self.call_failed()
            raise RuntimeError('call is not set')
        self.b = randint(2, self.dhc.p-1)
        self.g_b = pow(self.dhc.g, self.b, self.dhc.p)
        self.check_g(self.g_b, self.dhc.p)
        self.g_a_hash = self.call.g_a_hash
        try:
            self.call = self._client.send(functions.phone.AcceptCall(
                peer=types.InputPhoneCall(id=self.call_id, access_hash=self.call_access_hash),
                g_b=i2b(self.g_b),
                protocol=self.protocol
            )).phone_call
        except errors.CallAlreadyAccepted:
            self.stop()
            return True
        except errors.CallAlreadyDeclined:
            self.call_discarded()
            return False
        if isinstance(self.call, types.PhoneCallDiscarded):
            print('Call is already discarded')
            self.call_discarded()
            return False
        return True

    def call_accepted(self) -> None:
        # for handler in self.call_accepted_handlers:
        #     callable(handler) and handler(self)

        if not self.call.g_a_or_b:
            print('g_a is null')
            self.call_failed()
            return
        if self.g_a_hash != hashlib.sha256(self.call.g_a_or_b).digest():
            print('g_a_hash doesn\'t match')
            self.call_failed()
            return
        self.g_a = b2i(self.call.g_a_or_b)
        self.check_g(self.g_a, self.dhc.p)
        self.auth_key = pow(self.g_a, self.b, self.dhc.p)
        self.key_fingerprint = calc_fingerprint(self.auth_key_bytes)
        if self.key_fingerprint != self.call.key_fingerprint:
            print('fingerprints don\'t match')
            self.call_failed()
            return
        self._initiate_encrypted_call()
