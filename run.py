import hashlib

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

define("host", default="8888", help="端口")


class WxHandler(RequestHandler):
    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            token = "LiJiaF"

            wxList = [token, timestamp, nonce]
            wxList.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, wxList)
            hashcode = sha1.hexdigest()

            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as err:
            return err


def make_app():
    return Application([
        (r"/wx", WxHandler),
    ])


if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(options.host)
    IOLoop.current().start()
