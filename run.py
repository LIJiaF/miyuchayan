import hashlib
import os
import math
import random
import json

from datetime import datetime, timedelta
from urllib import request

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

import receive
import reply
from basic import Basic
from wxConfig import APPID, APPSECRET
from common.redisConn import redis
from common.postgresqlConn import Postgres
from common.log_print import logger
from common.wrapper_func import wrapper_allow_origin_func

define("host", default="8888", help="端口")


class IndexHandler(RequestHandler):
    def get(self):
        # conn = Postgres()
        # sql = """
        #     select openid, username, image_url, province, city, score, discount, date
        #     from wx_user
        #     where openid = '%s'
        # """ % 'oBGCb1GE38DXO03ebeY0MtnfJKmc'
        # data = conn.fetchone(sql)
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
                            content = '对不起，该功能暂未对外开放！'
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            self.write(replyMsg.send())
                else:
                    self.write(reply.Msg().send())
        except Exception as err:
            return err


class DiscountHandler(RequestHandler):
    def get(self):
        code = self.get_argument('code', None)
        logger.info('code: %s' % code)
        get_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
            APPID, APPSECRET, code)
        token_data = json.loads(request.urlopen(url=get_token_url).read())
        if token_data.get('errcode'):
            logger.error('errcode: %s' % token_data['errcode'])
            logger.error('errmsg: %s' % token_data['errmsg'])
            return self.write('获取网页access_token失败，请在微信端打开')

        access_token = token_data.get('access_token', None)
        refresh_token = token_data.get('refresh_token', None)
        openid = token_data.get('openid', None)
        logger.info('access_token: %s', access_token)
        logger.info('refresh_token: %s', refresh_token)
        logger.info('openid: %s', openid)

        # 检验access_token是否有效
        check_token_url = 'https://api.weixin.qq.com/sns/auth?access_token=%s&openid=%s' % (access_token, openid)
        chekc_token_data = json.loads(request.urlopen(url=check_token_url).read())
        if chekc_token_data.get('errcode'):
            refresh_token_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s' % (
                APPID, refresh_token)
            refresh_data = json.loads(request.urlopen(url=refresh_token_url).read())
            if not refresh_data.get('errcode'):
                logger.info('重新获取access_token、openid')
                access_token = refresh_data.get('access_token', None)
                openid = refresh_data.get('openid', None)
                logger.info('access_token: %s', access_token)
                logger.info('openid: %s', openid)

        # openid = 'oBGCb1GE38DXO03ebeY0MtnfJKmc'

        conn = Postgres()
        sql = """
            select wd.id,name,type,discount,score,count,rule
            from wx_discount as wd
            inner join wx_discount_type as wdt on wd.type_id = wdt.id
            where state = true and count > 0
        """
        data = conn.fetchall(sql)

        return self.render('discount.html', data=data, openid=openid)

    @wrapper_allow_origin_func
    def post(self):
        discount_id = self.get_argument('discount_id', None)
        openid = self.get_argument('openid', None)

        res = {
            'code': 0
        }

        if not discount_id or not openid:
            res['code'] = -1
            res['msg'] = '领取失败'
            return self.finish(res)

        conn = Postgres()
        sql = "select * from wx_user_discount_rel where discount_id = %d and state = false" % int(discount_id)
        count = conn.fetchall(sql)
        if len(count) >= 2:
            res['code'] = -1
            res['msg'] = '每种类型优惠券只能领取两张，请使用后再领取！'
            return self.finish(res)

        discount = conn.fetchone("select count from wx_discount where id = %d" % int(discount_id))
        if discount['count'] <= 0:
            res['code'] = -1
            res['msg'] = '对不起，该优惠券已经被领完了！'
            return self.finish(res)

        user_score = conn.fetchone("select score from wx_user where openid = '%s'" % openid)
        discount_score = conn.fetchone("select score from wx_discount where id = %d" % int(discount_id))
        if not user_score or user_score['score'] < discount_score['score']:
            res['code'] = -1
            res['msg'] = '对不起，您的积分不够哦！'
            return self.finish(res)

        try:
            end_time = datetime.strftime(datetime.now() + timedelta(days=7), '%Y-%m-%d')
            sql = """
                insert into wx_user_discount_rel (openid, discount_id, end_time)
                values ('%s', %d, '%s');
            """ % (openid, int(discount_id), end_time)
            sql += """
                update wx_discount set count = count - 1
                where id = %d;
            """ % int(discount_id)
            sql += """
                update wx_user set score = score - %d
                where openid = '%s';
            """ % (discount_score['score'], openid)
            conn.execute(sql)

            res['msg'] = '领取成功'
            return self.finish(res)
        except Exception:
            res['code'] = -1
            res['msg'] = '领取失败'
            return self.finish(res)


class PersonalHandler(RequestHandler):
    def get(self):
        # 根据code获取网页access_token和openid
        code = self.get_argument('code', None)
        logger.info('code: %s' % code)
        get_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
            APPID, APPSECRET, code)
        token_data = json.loads(request.urlopen(url=get_token_url).read())
        if token_data.get('errcode'):
            logger.error('errcode: %s' % token_data['errcode'])
            logger.error('errmsg: %s' % token_data['errmsg'])
            return self.write('获取网页access_token失败，请在微信端打开')

        access_token = token_data.get('access_token', None)
        refresh_token = token_data.get('refresh_token', None)
        openid = token_data.get('openid', None)
        logger.info('access_token: %s', access_token)
        logger.info('refresh_token: %s', refresh_token)
        logger.info('openid: %s', openid)

        # 检验access_token是否有效
        check_token_url = 'https://api.weixin.qq.com/sns/auth?access_token=%s&openid=%s' % (access_token, openid)
        chekc_token_data = json.loads(request.urlopen(url=check_token_url).read())
        if chekc_token_data.get('errcode'):
            refresh_token_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s' % (
                APPID, refresh_token)
            refresh_data = json.loads(request.urlopen(url=refresh_token_url).read())
            if not refresh_data.get('errcode'):
                logger.info('重新获取access_token、openid')
                access_token = refresh_data.get('access_token', None)
                openid = refresh_data.get('openid', None)
                logger.info('access_token: %s', access_token)
                logger.info('openid: %s', openid)

        # 根据access_token和openid获取用户信息
        get_info_url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (
            access_token, openid)
        info_data = json.loads(request.urlopen(url=get_info_url).read())
        if info_data.get('errcode'):
            logger.error('errcode: %s' % token_data['errcode'])
            logger.error('errmsg: %s' % token_data['errmsg'])
            return self.write('获取用户信息失败')

        conn = Postgres()
        data = conn.fetchone("select id from wx_user where openid = '%s'" % openid)
        logger.info('查看数据库是否存在该用户信息: %s' % data)
        if not data:
            sql = """
                insert into wx_user (openid, username, image_url, province, city)
                values ('%s', '%s', '%s', '%s', '%s');
            """ % (openid, info_data.get('nickname'), info_data.get('headimgurl'), info_data.get('province'),
                   info_data.get('city'))
            end_time = datetime.strftime(datetime.now() + timedelta(days=7), '%Y-%m-%d')
            sql += """
                insert into wx_user_discount_rel (openid, discount_id, end_time)
                values ('%s', %d, '%s');
            """ % (openid, 1, end_time)
            conn.execute(sql)
        else:
            sql = """
                update wx_user
                set username = '%s', image_url = '%s', province = '%s', city = '%s'
                where openid = '%s'
            """ % (info_data.get('nickname'), info_data.get('headimgurl'), info_data.get('province'),
                   info_data.get('city'), openid)
            conn.execute(sql)

        # conn = Postgres()
        # openid = 'oBGCb1GE38DXO03ebeY0MtnfJKmc'

        user_sql = """
            select openid, username, image_url, province, city, score, date
            from wx_user 
            where openid = '%s'
        """ % openid
        user_data = conn.fetchone(user_sql)

        discount_sql = """
            select wd.id,discount,name,end_time,type,rule
            from wx_user_discount_rel as wud
            left join wx_discount as wd on wd.id = wud.discount_id
            inner join wx_discount_type as wdt on wdt.id = wd.type_id
            where openid = '%s' and wud.state = false
            order by id desc
        """ % openid
        discount_data = conn.fetchall(discount_sql)

        info = {
            'openid': user_data['openid'],
            'username': user_data['username'] or '密语君',
            'province': user_data['province'] or '保密',
            'city': user_data['city'] or '保密',
            'image_url': user_data['image_url'],
            'score': user_data['score'],
            'discount': len(discount_data),
            'discount_list': discount_data,
            'is_receive': user_data['date'] >= datetime.strftime(datetime.now(), '%Y-%m-%d')
        }
        logger.info('用户信息: %s' % info)

        return self.render('personal.html', info=info)

    @wrapper_allow_origin_func
    def post(self):
        openid = self.get_argument('openid', None)
        res = {
            'code': 0
        }
        print(openid)
        if openid:
            now = datetime.strftime(datetime.now(), '%Y-%m-%d')
            conn = Postgres()
            data = conn.fetchone("select date from wx_user where openid = '%s'" % openid)
            if data['date'] and data['date'] == now:
                res['code'] = -1
                res['msg'] = '积分领取失败'
                return self.finish(res)
            conn.execute("update wx_user set score = score + 5, date = '%s' where openid = '%s'" % (now, openid))
            res['msg'] = '积分领取成功'
            return self.finish(res)

        res['code'] = -1
        res['msg'] = '积分领取失败'
        return self.finish(res)


class UploadHandler(RequestHandler):
    def get(self):
        accessToken = Basic().get_access_token()
        return self.render('upload.html', accessToken=accessToken)

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
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'template_path': os.path.join(os.path.dirname(__file__), 'template')
    }

    return Application([
        (r"/", IndexHandler),
        (r"/wx", WxHandler),
        (r"/discount/*", DiscountHandler),
        (r"/personal/*", PersonalHandler),
        (r"/upload", UploadHandler),
    ], **config)


if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(options.host)
    IOLoop.current().start()
