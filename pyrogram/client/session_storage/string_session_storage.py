import base64
import binascii
import struct

from . import BaseSessionStorage, SessionDoesNotExist


class StringSessionStorage(BaseSessionStorage):
    """
    Packs session data as following (forcing little-endian byte order):
    Char dc_id (1 byte, unsigned)
    Boolean test_mode (1 byte)
    Long long user_id (8 bytes, signed)
    Bytes auth_key (256 bytes)

    Uses Base64 encoding for printable representation
    """
    PACK_FORMAT = '<B?q256s'

    def load_session(self):
        try:
            session_string = self.session_data[1:]
            session_string += '=' * (4 - len(session_string) % 4)  # restore padding
            decoded = base64.b64decode(session_string, b'-_')
            self.dc_id, self.test_mode, self.user_id, self.auth_key = struct.unpack(self.PACK_FORMAT, decoded)
        except (struct.error, binascii.Error):
            raise SessionDoesNotExist()

    def save_session(self, sync=False):
        if not sync:
            packed = struct.pack(self.PACK_FORMAT, self.dc_id, self.test_mode, self.user_id, self.auth_key)
            encoded = ':' + base64.b64encode(packed, b'-_').decode('latin-1').rstrip('=')
            split = '\n'.join(['"{}"'.format(encoded[i: i + 50]) for i in range(0, len(encoded), 50)])
            print('Created session string:\n{}'.format(split))

    def sync_cleanup(self):
        pass
