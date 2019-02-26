import pyrogram
from pyrogram.api import types
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
        self._peers_cache = {}

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

    def clear_cache(self):
        keys = list(filter(lambda k: k[0] in 'up', self._peers_cache.keys()))
        for key in keys:
            try:
                del self._peers_cache[key]
            except KeyError:
                pass

    def cache_peer(self, entity):
        if isinstance(entity, types.User):
            input_peer = types.InputPeerUser(
                user_id=entity.id,
                access_hash=entity.access_hash
            )
            self._peers_cache['i' + str(entity.id)] = input_peer
            if entity.username:
                self._peers_cache['u' + entity.username.lower()] = input_peer
            if entity.phone:
                self._peers_cache['p' + entity.phone] = input_peer
        elif isinstance(entity, (types.Chat, types.ChatForbidden)):
            self._peers_cache['i-' + str(entity.id)] = types.InputPeerChat(chat_id=entity.id)
        elif isinstance(entity, (types.Channel, types.ChannelForbidden)):
            input_peer = types.InputPeerChannel(
                channel_id=entity.id,
                access_hash=entity.access_hash
            )
            self._peers_cache['i-100' + str(entity.id)] = input_peer
            username = getattr(entity, "username", None)
            if username:
                self._peers_cache['u' + username.lower()] = input_peer

    def get_peer_by_id(self, val):
        return self._peers_cache['i' + str(val)]

    def get_peer_by_username(self, val):
        return self._peers_cache['u' + val.lower()]

    def get_peer_by_phone(self, val):
        return self._peers_cache['p' + val]

    def peers_count(self):
        return len(list(filter(lambda k: k[0] == 'i', self._peers_cache.keys())))

    def contacts_count(self):
        return len(list(filter(lambda k: k[0] == 'p', self._peers_cache.keys())))
