import json

from tornado.web import RequestHandler

from common.wrapper_func import is_login_func
from common.postgresql_conn import Postgres


class AdminUserHandler(RequestHandler):
    @is_login_func
    def get(self):
        sql = """
            select id, username, image_url, city, score, experience, is_admin
            from wx_user
        """
        conn = Postgres()
        data = conn.fetchall(sql)

        return self.finish(json.dumps(data))
