import hashlib
import time

from tornado.web import RequestHandler

from common.postgresql_conn import Postgres
from common.log_print import logger


class AdminLoginHandler(RequestHandler):
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

        password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
        conn = Postgres()
        sql = """
            select id 
            from admin_user 
            where username = '%s' 
            and password = '%s'
        """ % (username, password_md5)
        user = conn.fetchone(sql)

        if not user:
            res['code'] = -1
            res['msg'] = '账号或密码错误！'
        else:
            res['msg'] = '登录成功！'
            self.set_secure_cookie('username', username, expires=time.time() + (30 * 60))

        return self.finish(res)


class AdminRegisterHandler(RequestHandler):
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
        if user:
            res['code'] = -1
            res['msg'] = '该用户已经存在！'
            return self.finish(res)

        password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
        try:
            sql = """
                insert into admin_user (username, password)
                values ('%s', '%s')
            """ % (username, password_md5)
            conn.execute(sql)
            res['msg'] = '用户注册成功！'
        except Exception as e:
            res['code'] = -1
            res['msg'] = '用户注册失败！'
            logger.error(e)
        finally:
            return self.finish(res)
