import pyrogram
from . import SessionStorage, SessionDoesNotExist


class MemorySessionStorage(SessionStorage):
    def __init__(self, client: 'pyrogram.client.ext.BaseClient'):
        super(MemorySessionStorage, self).__init__(client)
        self._dc_id = 1
        self._test_mode = None
        self._auth_key = None
        self._user_id = None
        self._date = 0
        self._is_bot = False
        self._peers_by_id = {}
        self._peers_by_username = {}
        self._peers_by_phone = {}

    def load(self):
        raise SessionDoesNotExist()

    def save(self, sync=False):
        pass

    def sync_cleanup(self):
        pass

    @property
    def dc_id(self):
        return self._dc_id

    @dc_id.setter
    def dc_id(self, val):
        self._dc_id = val

    @property
    def test_mode(self):
        return self._test_mode

    @test_mode.setter
    def test_mode(self, val):
        self._test_mode = val

    @property
    def auth_key(self):
        return self._auth_key

    @auth_key.setter
    def auth_key(self, val):
        self._auth_key = val

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, val):
        self._user_id = val

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, val):
        self._date = val

    @property
    def is_bot(self):
        return self._is_bot

    @is_bot.setter
    def is_bot(self, val):
        self._is_bot = val

    @property
    def peers_by_id(self):
        return self._peers_by_id

    @property
    def peers_by_username(self):
        return self._peers_by_username

    @property
    def peers_by_phone(self):
        return self._peers_by_phone
