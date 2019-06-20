import psycopg2

from .log_print import logger


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
        row = cur.fetchone()
        self.close(cur, conn)

        return dict(zip(columns, row)) if row else row

    def fetchall(self, sql):
        conn = self.get_connect()
        cur = conn.cursor()
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        rows = cur.fetchall()
        self.close(cur, conn)

        return [dict(zip(columns, row)) for row in rows] if rows else rows

    def execute(self, sql):
        conn = self.get_connect()
        cur = conn.cursor()
        try:
            logger.info('执行sql语句: %s' % sql)
            cur.execute(sql)
            conn.commit()
        except Exception:
            logger.error('执行sql语句失败: %s' % sql)
        finally:
            self.close(cur, conn)

    def close(self, cur, conn):
        cur.close()
        conn.close()
