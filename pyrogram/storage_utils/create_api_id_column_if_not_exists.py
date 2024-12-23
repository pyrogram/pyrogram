from sqlite3 import Connection


def create_api_id_column_if_not_exists(conn: Connection):
    res = conn.execute('pragma table_info(sessions)')
    api_id_row = next((r for r in res if r[1] == 'api_id'), None)
    if not api_id_row:
        conn.execute('alter table sessions add column api_id integer')
        conn.execute('update sessions SET api_id = 2496')
