import hashlib

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

import receive
import reply

define("host", default="8888", help="端口")


class WxHandler(RequestHandler):
    # 微信公众号接入验证
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

    # 收发消息处理
    def post(self):
        try:
            webData = self.request.body
            print(webData)
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                # 文本信息处理
                if recMsg.MsgType == 'text':
                    content = "test"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    self.write(replyMsg.send())
                # 图片信息处理
                elif recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    self.write(replyMsg.send())
                elif recMsg.MsgType == 'event':
                    print(recMsg.Event)
                    print(recMsg.EventKey)
                    content = 'event'
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    self.write(replyMsg.send())
                else:
                    self.write(reply.Msg().send())
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
