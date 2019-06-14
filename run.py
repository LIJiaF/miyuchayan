import hashlib
import os
import math
import random
import json
from datetime import datetime

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

import receive
import reply
from basic import Basic
from redisConn import redis

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
                    # 关注公众号事件
                    if recMsg.Event == 'subscribe':
                        content = '欢迎您'
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        self.write(replyMsg.send())
                    # 菜单点击事件
                    elif recMsg.Event == 'CLICK':
                        eventKey = recMsg.EventKey
                        if eventKey == 'history':
                            content = eventKey
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            self.write(replyMsg.send())
                        elif eventKey == 'personal':
                            title = '测试图文消息'
                            description = '测试图文消息'
                            picUrl = 'https://www.baidu.com/img/bd_logo1.png?where=super'
                            url = 'https://www.baidu.com/'
                            replyMsg = reply.ArticleMsg(toUser, fromUser, title, description, picUrl, url)
                            self.write(replyMsg.send())
                else:
                    self.write(reply.Msg().send())
        except Exception as err:
            return err


class DiscountHandler(RequestHandler):
    def get(self):
        return self.write('this is discount view')


class UploadHandler(RequestHandler):
    def get(self):
        accessToken = Basic().get_access_token()
        return self.render('index.html', accessToken=accessToken)

    def post(self):
        files = self.request.files.get('img', None)
        if files:
            if not files:
                return self.write('上传图片不能为空')

            upload_path = os.path.join(os.path.dirname(__file__), 'upload')
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)

            for file in files:
                if file['content_type'] not in ['image/png', 'image/jpeg']:
                    return self.write('上传图片格式有误')

                try:
                    name = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + str(math.floor(random.random() * 10))
                    sName = name + '.' + file['filename'].split('.')[1]
                    with open(os.path.join(upload_path, sName), 'wb') as up:
                        up.write(file['body'])

                    accessToken = Basic().get_access_token()
                    cmd = 'curl -F media=@upload/%s "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=%s"' % (
                        sName, accessToken)
                    wxName = json.loads(os.popen(cmd).read())['url']
                    fName = file['filename']

                    redis.hmset('wx:' + name, {'sname': sName, 'wxname': wxName, 'fname': fName})
                except Exception:
                    print(file['filename'] + '文件上传失败')

            return self.write('图片上传成功')


def make_app():
    config = {
        'template_path': os.path.join(os.path.dirname(__file__), 'template')
    }

    return Application([
        (r"/", IndexHandler),
        (r"/wx", WxHandler),
        (r"/discount/", DiscountHandler),
        (r"/upload", UploadHandler),
    ], **config)


if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(options.host)
    IOLoop.current().start()
