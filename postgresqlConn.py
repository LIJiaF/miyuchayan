import psycopg2


class Postgres(object):
    def __init__(self):
        self.database = 'wx'
        self.user = 'postgres'
        self.password = 'root'
        self.host = 'localhost'
        self.port = 5432

    def get_connect(self):
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host,
                                port=self.port)

        return conn

    def select(self, sql):
        conn = self.get_connect()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        self.close(cur, conn)

        return rows

    def execute(self, sql):
        conn = self.get_connect()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except Exception:
            print('sql执行失败')
        finally:
            self.close(cur, conn)

    def close(self, cur, conn):
        cur.close()
        conn.close()
