import hashlib

from tornado.web import RequestHandler

from common.postgresql_conn import Postgres
from common.log_print import logger
from common.wrapper_func import is_login_func


class AdminEditPasswordHandler(RequestHandler):
    @is_login_func
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        res = {
            'code': 0
        }

        if not username or not password:
            res['code'] = -1
            res['msg'] = '账号或密码不能为空！'
            return self.finish(res)

        conn = Postgres()
        user = conn.fetchone("select id from admin_user where username = '%s'" % username)
        if not user:
            res['code'] = -1
            res['msg'] = '该用户不存在！'
            return self.finish(res)

        password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
        try:
            sql = """
                update admin_user
                set password = '%s'
                where id = %d
            """ % (password_md5, user['id'])
            conn.execute(sql)
            res['msg'] = '密码修改成功！'
        except Exception as e:
            res['code'] = -1
            res['msg'] = '密码修改失败！'
            logger.error(e)
        finally:
            return self.finish(res)
