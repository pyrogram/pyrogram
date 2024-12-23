import base64
import gzip

from pyrogram.storage import Storage
from pyrogram.storage.sql_dump_memory_storage import SqlDumpMemoryStorage


def create_storage_from_sql_dump_base64_gz(session_gz_base64: str):
    decoded_from_base64 = base64.b64decode(session_gz_base64)
    decoded_from_base64_and_gz = gzip.decompress(decoded_from_base64).decode('utf-8')
    return SqlDumpMemoryStorage(decoded_from_base64_and_gz)


async def create_sql_dump_base64_gz_dump(storage: SqlDumpMemoryStorage or Storage):
    if not isinstance(storage, SqlDumpMemoryStorage):
        raise 'Unsupported storage type, expected SqlDumpMemoryStorage'
    sql = await storage.dump()
    encoded_with_gz = gzip.compress(sql.encode('utf-8'), 9)
    encoded_with_gz_and_base64 = base64.b64encode(encoded_with_gz).decode('utf-8')
    return str(encoded_with_gz_and_base64)
