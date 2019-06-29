import hashlib
import os

from tornado.web import RequestHandler, Application, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

from wx import receive, reply
from api import *
from basic import Basic
from sign import Sign
from common.log_print import logger

define("host", default="8888", help="端口")


class IndexHandler(RequestHandler):
    def get(self):
        return self.write('this is index view')


class WxHandler(RequestHandler):
    # 微信公众号接入验证
    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            token = "LiJiaF"

            tmp = [token, timestamp, nonce]
            tmp.sort()
            tmp = "".join(tmp)
            hashcode = hashlib.sha1(tmp.encode('utf8')).hexdigest()

            if hashcode == signature:
                logger.info('微信公众号接入成功')
                self.write(echostr)
            else:
                logger.error('微信公众号接入失败')
                self.write('')
        except Exception as err:
            self.write(err)

    # 收发消息处理
    def post(self):
        try:
            webData = self.request.body
            logger.info('接收信息: %s' % webData)
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                # 文本信息处理
                if recMsg.MsgType == 'text':
                    content = "好的，密语君会尽快为您处理^_^"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    self.write(replyMsg.send())
                # 图片信息处理
                elif recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    self.write(replyMsg.send())
                elif recMsg.MsgType == 'event':
                    # 关注公众号事件
                    if recMsg.Event == 'subscribe':
                        content = '您好，欢迎关注密语君^_^\n更多优惠请留意粉丝福利！'
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        self.write(replyMsg.send())
                    # 菜单点击事件
                    elif recMsg.Event == 'CLICK':
                        eventKey = recMsg.EventKey
                        print('点击事件：', eventKey)
                        if eventKey == 'phone':
                            content = '139 2829 0304'
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            self.write(replyMsg.send())
                        elif eventKey == 'score_rule':
                            content = """积分说明：
1. 每天登陆可领取5积分
2. 每使用一张优惠券可增加20积分
3. 积分可以兑换优惠券"""
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            self.write(replyMsg.send())
                else:
                    self.write(reply.Msg().send())
        except Exception as err:
            return err


class signatureHandler(RequestHandler):
    def get(self):
        url = self.get_argument('fullUrl', None)
        jsapi_ticket = Basic.get_jsapi_ticket()
        logger.info('url：%s' % url)
        logger.info('jsapi_ticket：%s' % jsapi_ticket)

        sign = Sign(jsapi_ticket, url)
        res = sign.sign()
        logger.info('res：%s' % res)

        return self.finish(res)


def make_app():
    config = {
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'template_path': os.path.join(os.path.dirname(__file__), 'template')
    }

    return Application([
        (r"/", IndexHandler),
        (r"/wx", WxHandler),
        (r"/discount", DiscountHandler),
        (r"/personal", PersonalHandler),
        (r"/scan", ScanHandler),
        (r"/upload", UploadHandler),
        (r"/signature", signatureHandler),
        (r"/(.*)", StaticFileHandler,
         {"path": config['static_path'], "default_filename": "MP_verify_VUv3rv3xeIyo7z8I.txt"})
    ], **config)


if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(options.host)
    IOLoop.current().start()
