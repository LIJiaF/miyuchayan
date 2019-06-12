import hashlib

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

import receive
import reply

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
                print('微信公众号接入成功')
                self.write(echostr)
            else:
                self.write('')
        except Exception as err:
            self.write(err)

    def post(self):
        try:
            webData = self.request
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "test"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                self.write(replyMsg.send())
            else:
                self.write('success')
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
