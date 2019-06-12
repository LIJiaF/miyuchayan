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

            print('signature: ', signature)
            print('timestamp: ', timestamp)
            print('nonce: ', nonce)
            print('echostr: ', echostr)

            tmp = [token, timestamp, nonce]
            tmp.sort()
            tmp = "".join(tmp)
            hashcode = hashlib.sha1(tmp.encode('utf8')).hexdigest()

            if hashcode == signature:
                print('success')
                self.write(echostr)
            else:
                self.write('')
        except Exception as err:
            self.write(err)


def make_app():
    return Application([
        (r"/wx", WxHandler),
    ])


if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(options.host)
    IOLoop.current().start()
