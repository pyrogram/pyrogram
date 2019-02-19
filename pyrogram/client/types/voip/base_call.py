# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

import pyrogram
from pyrogram.api import types, functions, errors
from ..pyrogram_type import PyrogramType
from ..update import Update
from tgvoip import VoIPController, CallState, CallError, VoIPServerConfig, DataSaving, Endpoint
from tgvoip.utils import b2i, i2b, get_real_elapsed_time, check_g


class DH:
    def __init__(self, p: bytes, g: int):
        self.p = b2i(p)
        self.g = g


class BaseCall(Update, PyrogramType):
    min_layer = 65
    max_layer = VoIPController.CONNECTION_MAX_LAYER
    outgoing = False
    protocol = types.PhoneCallProtocol(min_layer, max_layer, True, True)

    def __init__(self,
                 client: "pyrogram.client.ext.BaseClient",
                 use_proxy_if_available: bool = True):
        super(BaseCall, self).__init__(client)
        self.ctrl = VoIPController()
        self.ctrl_started = False
        self.call = None
        self.peer = None
        self.state = None
        self.dhc = self.get_dhc()
        self.a = None
        self.g_a = None
        self.g_a_hash = None
        self.b = None
        self.g_b = None
        self.g_b_hash = None
        self.auth_key = None
        self.key_fingerprint = None

        if use_proxy_if_available and client.proxy:
            p = client.proxy
            self.ctrl.set_proxy(p['hostname'], p['port'], p['username'], p['password'])

        self._update_handler = pyrogram.PhoneCallHandler(self._process_update)
        client.add_handler(self._update_handler, -1)

    def __del__(self):
        self.discard()

    def _process_update(self, client, call):
        if not self.call or not call or call.id != self.call.id:
            raise pyrogram.ContinuePropagation
        if not hasattr(call, 'access_hash') or not call.access_hash:
            call.access_hash = self.call.access_hash
        self.call = call

        if isinstance(call, types.PhoneCallDiscarded):
            self.call_discarded()
            raise pyrogram.StopPropagation

    @property
    def auth_key_bytes(self) -> bytes:
        return i2b(self.auth_key) if self.auth_key is not None else b''

    @property
    def call_id(self) -> int:
        return self.call.id if self.call else 0

    def get_dhc(self) -> DH:
        dhc = self._client.send(functions.messages.GetDhConfig(0, 256))
        return DH(dhc.p, dhc.g)

    def check_g(self, g_x: int, p: int) -> None:
        try:
            check_g(g_x, p)
        except RuntimeError:
            self.call_discarded()
            raise

    def stop(self) -> None:
        try:
            self._client.remove_handler(self._update_handler, -1)
        except ValueError:
            pass
        del self.ctrl
        self.ctrl = None
        try:
            self._client.calls.remove(self)
        except ValueError:
            pass

        # for handler in self.call_ended_handlers:
        #     callable(handler) and handler(self)

    def update_state(self, val: CallState) -> None:
        self.state = val
        self.ctrl.update_state(val)

    def call_ended(self) -> None:
        self.update_state(CallState.ENDED)
        self.stop()

    def call_failed(self, error: CallError = None) -> None:
        if error is None:
            error = self.ctrl.get_last_error() if self.ctrl and self.ctrl_started else CallError.UNKNOWN
        print('Call', self.call_id, 'failed with error', error)
        self.update_state(CallState.FAILED)
        self.stop()

    def call_discarded(self):
        # TODO: call.need_debug
        need_rate = self.ctrl and VoIPServerConfig.config.get('bad_call_rating') and self.ctrl.need_rate()
        if isinstance(self.call.reason, types.PhoneCallDiscardReasonBusy):
            self.update_state(CallState.BUSY)
            self.stop()
        else:
            self.call_ended()
        if self.call.need_rating or need_rate:
            pass  # TODO: rate

        # for handler in self.call_discarded_handlers:
        #     callable(handler) and handler(self)

    def discard(self, reason=types.PhoneCallDiscardReasonDisconnect()):
        # TODO: rating
        try:
            self._client.send(functions.phone.DiscardCall(
                peer=types.InputPhoneCall(self.call_id, self.call.access_hash),
                duration=int(get_real_elapsed_time() - (self.ctrl.start_time or 0)),
                connection_id=self.ctrl.get_preferred_relay_id(),
                reason=reason
            ))
        except (errors.CallAlreadyDeclined, errors.CallAlreadyAccepted):
            pass
        self.call_ended()

    def _initiate_encrypted_call(self) -> None:
        config = self._client.send(functions.help.GetConfig())  # type: types.Config
        self.ctrl.set_config(config.call_packet_timeout_ms / 1000., config.call_connect_timeout_ms / 1000.,
                             DataSaving.NEVER, self.call.id)
        self.ctrl.set_encryption_key(self.auth_key_bytes, self.outgoing)
        endpoints = [self.call.connection] + self.call.alternative_connections
        endpoints = [Endpoint(e.id, e.ip, e.ipv6, e.port, e.peer_tag) for e in endpoints]
        self.ctrl.set_remote_endpoints(endpoints, self.call.p2p_allowed, False, self.call.protocol.max_layer)
        self.ctrl.start()
        self.ctrl.connect()
        self.ctrl_started = True
        self.update_state(CallState.ESTABLISHED)

        # for handler in self.call_started_handlers:
        #     callable(handler) and handler(self)
