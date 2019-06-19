from functools import wraps


# 支持跨域
def wrapper_allow_origin_func(func):
    @wraps(func)
    def __wrapper__(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        return func(self, *args, **kwargs)

    return __wrapper__
