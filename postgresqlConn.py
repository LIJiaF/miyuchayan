import psycopg2


class Postgres(object):
    def __init__(self):
        self.database = 'postgres'
        self.user = 'postgres'
        self.password = 'root'
        self.host = '120.76.56.231'
        self.port = 5432

    def get_connect(self):
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host,
                                port=self.port)

        return conn

    def fetchone(self, sql):
        conn = self.get_connect()
        cur = conn.cursor()
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        row = [str(row) for row in cur.fetchone()]
        result = dict(zip(columns, row))

        self.close(cur, conn)

        return result

    def fetchall(self, sql):
        conn = self.get_connect()
        cur = conn.cursor()
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        rows = [[str(item) for item in row] for row in cur.fetchall()]
        result = [dict(zip(columns, row)) for row in rows]

        self.close(cur, conn)

        return result

    def execute(self, sql):
        conn = self.get_connect()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except Exception:
            print('sql执行失败: ', sql)
        finally:
            self.close(cur, conn)

    def close(self, cur, conn):
        cur.close()
        conn.close()
