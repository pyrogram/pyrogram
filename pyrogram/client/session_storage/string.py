import base64
import binascii
import struct

import pyrogram
from . import MemorySessionStorage, SessionDoesNotExist


class StringSessionStorage(MemorySessionStorage):
    """
    Packs session data as following (forcing little-endian byte order):
    Char dc_id (1 byte, unsigned)
    Boolean test_mode (1 byte)
    Long long user_id (8 bytes, signed)
    Boolean is_bot (1 byte)
    Bytes auth_key (256 bytes)

    Uses Base64 encoding for printable representation
    """
    PACK_FORMAT = '<B?q?256s'

    def __init__(self, client: 'pyrogram.client.ext.BaseClient', session_string: str):
        super(StringSessionStorage, self).__init__(client)
        self._session_string = session_string

    def _unpack(self, data):
        return struct.unpack(self.PACK_FORMAT, data)

    def _pack(self):
        return struct.pack(self.PACK_FORMAT, self._dc_id, self._test_mode, self._user_id, self._is_bot, self._auth_key)

    def load(self):
        try:
            session_string = self._session_string[1:]
            session_string += '=' * (4 - len(session_string) % 4)  # restore padding
            decoded = base64.b64decode(session_string, b'-_')
            self._dc_id, self._test_mode, self._user_id, self._is_bot, self._auth_key = self._unpack(decoded)
        except (struct.error, binascii.Error):
            raise SessionDoesNotExist()

    def save(self, sync=False):
        if not sync:
            packed = self._pack()
            encoded = ':' + base64.b64encode(packed, b'-_').decode('latin-1').rstrip('=')
            split = '\n'.join(['"{}"'.format(encoded[i: i + 50]) for i in range(0, len(encoded), 50)])
            print('Created session string:\n{}'.format(split))
