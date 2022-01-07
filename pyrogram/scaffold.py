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
import os
import platform
import re
import sys
from io import StringIO
from mimetypes import MimeTypes
from pathlib import Path

import pyrogram
from pyrogram import __version__
from pyrogram.parser import Parser
from pyrogram.session.internals import MsgId
from .mime_types import mime_types


class Scaffold:
    APP_VERSION = f"Pyrogram {__version__}"
    DEVICE_MODEL = f"{platform.python_implementation()} {platform.python_version()}"
    SYSTEM_VERSION = f"{platform.system()} {platform.release()}"

    LANG_CODE = "en"

    PARENT_DIR = Path(sys.argv[0]).parent

    INVITE_LINK_RE = re.compile(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:joinchat/|\+))([\w-]+)$")
    WORKERS = min(32, os.cpu_count() + 4)
    WORKDIR = PARENT_DIR
    CONFIG_FILE = PARENT_DIR / "config.ini"

    PARSE_MODES = ["combined", "markdown", "md", "html", None]

    mimetypes = MimeTypes()
    mimetypes.readfp(StringIO(mime_types))

    def __init__(self):
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            # This happens when creating Client instances inside different threads that don't have an event loop.
            # Set the main event loop in this thread.
            asyncio.set_event_loop(pyrogram.main_event_loop)

        self.session_name = None
        self.api_id = None
        self.api_hash = None
        self.app_version = None
        self.device_model = None
        self.system_version = None
        self.lang_code = None
        self.ipv6 = None
        self.proxy = None
        self.test_mode = None
        self.bot_token = None
        self.phone_number = None
        self.phone_code = None
        self.password = None
        self.force_sms = None
        self.workers = None
        self.workdir = None
        self.config_file = None
        self.plugins = None
        self.parse_mode = None
        self.no_updates = None
        self.takeout = None
        self.sleep_threshold = None

        self.executor = None

        self.storage = None

        self.rnd_id = MsgId

        self.parser = Parser(self)
        self.parse_mode = "combined"

        self.session = None

        self.media_sessions = {}
        self.media_sessions_lock = asyncio.Lock()

        self.is_connected = None
        self.is_initialized = None

        self.no_updates = None
        self.takeout_id = None

        self.dispatcher = None

        self.disconnect_handler = None

        self.loop = None

    async def send(self, *args, **kwargs):
        pass

    async def resolve_peer(self, *args, **kwargs):
        pass

    def fetch_peers(self, *args, **kwargs):
        pass

    def add_handler(self, *args, **kwargs):
        pass

    async def save_file(self, *args, **kwargs):
        pass

    async def get_messages(self, *args, **kwargs):
        pass

    async def get_history(self, *args, **kwargs):
        pass

    async def get_dialogs(self, *args, **kwargs):
        pass

    async def get_chat_members(self, *args, **kwargs):
        pass

    async def get_chat_members_count(self, *args, **kwargs):
        pass

    async def answer_inline_query(self, *args, **kwargs):
        pass

    async def get_profile_photos(self, *args, **kwargs):
        pass

    async def edit_message_text(self, *args, **kwargs):
        pass

    async def edit_inline_text(self, *args, **kwargs):
        pass

    async def edit_message_media(self, *args, **kwargs):
        pass

    async def edit_inline_media(self, *args, **kwargs):
        pass

    async def edit_message_reply_markup(self, *args, **kwargs):
        pass

    async def edit_inline_reply_markup(self, *args, **kwargs):
        pass

    def guess_mime_type(self, *args, **kwargs):
        pass

    def guess_extension(self, *args, **kwargs):
        pass

    def load_config(self, *args, **kwargs):
        pass

    def load_session(self, *args, **kwargs):
        pass

    def load_plugins(self, *args, **kwargs):
        pass

    async def handle_download(self, *args, **kwargs):
        pass

    async def start(self, *args, **kwargs):
        pass

    async def stop(self, *args, **kwargs):
        pass

    async def connect(self, *args, **kwargs):
        pass

    async def authorize(self, *args, **kwargs):
        pass

    async def disconnect(self, *args, **kwargs):
        pass

    async def initialize(self, *args, **kwargs):
        pass

    async def terminate(self, *args, **kwargs):
        pass
