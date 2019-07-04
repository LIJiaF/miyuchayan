from functools import wraps


# 支持跨域
def cross_domain_func(func):
    @wraps(func)
    def __wrapper__(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        return func(self, *args, **kwargs)

    return __wrapper__


# 验证登录状态
def is_login_func(func):
    @wraps(func)
    def __wrapper__(self, *args, **kwargs):
        user = self.get_secure_cookie('username')
        if user:
            return func(self, *args, **kwargs)
        else:
            # self.set_status(401)
            return func(self, *args, **kwargs)

    return __wrapper__
