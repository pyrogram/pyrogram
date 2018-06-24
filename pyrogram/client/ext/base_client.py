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

import platform
import re
from queue import Queue
from threading import Lock

from pyrogram import __version__
from ..style import Markdown, HTML
from ...api.core import Object
from ...session import Session
from ...session.internals import MsgId


class BaseClient:
    APP_VERSION = "Pyrogram \U0001f525 {}".format(__version__)

    DEVICE_MODEL = "{} {}".format(
        platform.python_implementation(),
        platform.python_version()
    )

    SYSTEM_VERSION = "{} {}".format(
        platform.system(),
        platform.release()
    )

    SYSTEM_LANG_CODE = "en"
    LANG_CODE = "en"

    INVITE_LINK_RE = re.compile(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/joinchat/)([\w-]+)$")
    BOT_TOKEN_RE = re.compile(r"^\d+:[\w-]+$")
    DIALOGS_AT_ONCE = 100
    UPDATES_WORKERS = 1
    DOWNLOAD_WORKERS = 1
    OFFLINE_SLEEP = 300

    MEDIA_TYPE_ID = {
        0: "thumbnail",
        1: "chat_photo",
        2: "photo",
        3: "voice",
        4: "video",
        5: "document",
        8: "sticker",
        9: "audio",
        10: "gif",
        13: "video_note"
    }

    def __init__(self):
        self.token = None
        self.dc_id = None
        self.auth_key = None
        self.user_id = None
        self.date = None

        self.rnd_id = MsgId
        self.channels_pts = {}

        self.peers_by_id = {}
        self.peers_by_username = {}
        self.peers_by_phone = {}

        self.markdown = Markdown(self.peers_by_id)
        self.html = HTML(self.peers_by_id)

        self.session = None
        self.media_sessions = {}
        self.media_sessions_lock = Lock()

        self.is_started = None
        self.is_idle = None

        self.updates_queue = Queue()
        self.updates_workers_list = []
        self.download_queue = Queue()
        self.download_workers_list = []

        self.disconnect_handler = None

    def send(self, data: Object, retries: int = Session.MAX_RETRIES, timeout: float = Session.WAIT_TIMEOUT):
        pass

    def resolve_peer(self, peer_id: int or str):
        pass

    def add_handler(self, handler, group: int = 0) -> tuple:
        pass

    def save_file(
            self,
            path: str,
            file_id: int = None,
            file_part: int = 0,
            progress: callable = None,
            progress_args: tuple = ()
    ):
        pass

    def get_messages(
            self,
            chat_id: int or str,
            message_ids,
            replies: int = 1
    ):
        pass
