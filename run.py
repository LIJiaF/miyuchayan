import os
import uuid

from tornado.web import RequestHandler, Application, StaticFileHandler
from tornado.options import define, options, parse_command_line
from tornado.ioloop import IOLoop

from api import *
from admin import *

define("host", default="8888", help="端口")


class IndexHandler(RequestHandler):
    def get(self):
        return self.write('this is index view')


def make_app():
    config = {
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'template_path': os.path.join(os.path.dirname(__file__), 'template'),
        'default_filename': 'MP_verify_VUv3rv3xeIyo7z8I.txt',
        'cookie_secret': str(uuid.uuid1())
    }

    wx_url = [
        (r"/", IndexHandler),
        (r"/wx", WxHandler),  # 微信接入
        (r"/discount", DiscountHandler),  # 粉丝福利
        (r"/personal", PersonalHandler),  # 个人中心
        (r"/scan", ScanHandler),  # 扫码
        (r"/qrcode", CodeHandler),  # 生成二维码
        (r"/upload", UploadHandler),  # 图片上传
        (r"/signature", signatureHandler),  # 微信jsdk接口配置
    ]

    admin_url = [
        (r"/admin/login", AdminLoginHandler),
        (r"/admin/register", AdminRegisterHandler),
        (r"/admin/user", AdminUserHandler),
    ]

    static_url = [
        (r"/(.*)", StaticFileHandler, {'path': config['static_path'], 'default_filename': config['default_filename']})
    ]

    return Application(wx_url + admin_url + static_url, **config)


if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(options.host)
    IOLoop.current().start()
