from tornado.web import RequestHandler

from common.wrapper_func import is_login_func


class AdminUserHandler(RequestHandler):
    @is_login_func
    def get(self):
        return self.write('user')
