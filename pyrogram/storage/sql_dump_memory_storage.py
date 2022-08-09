import sqlite3
from typing import Optional

from pyrogram.storage import MemoryStorage
from pyrogram.storage_utils.create_api_id_column_if_not_exists import create_api_id_column_if_not_exists


class SqlDumpMemoryStorage(MemoryStorage):
    __dump: str | None

    def __init__(self, dump: Optional[str] = None):
        super().__init__(':memory:')
        self.__dump = dump

    async def open(self):
        self.conn = sqlite3.connect(':memory:',
                                    check_same_thread=False)

        if self.__dump:
            self.conn.executescript(self.__dump)
        else:
            self.create()
        create_api_id_column_if_not_exists(self.conn)
        self.__dump = None

    async def dump(self) -> str:
        await self.save()
        self.conn.execute("delete from peers where (username is not null and username != '') or type == 'user';")
        return str.join('\n', self.conn.iterdump())
