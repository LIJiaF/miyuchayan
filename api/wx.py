import hashlib
from datetime import datetime, timedelta

from tornado.web import RequestHandler

from wx import receive, reply
from common.log_print import logger
from common.postgresql_conn import Postgres
from wx.basic import Basic


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
                # 事件处理
                elif recMsg.MsgType == 'event':
                    # 关注公众号事件
                    if recMsg.Event == 'subscribe':
                        logger.info('%s 关注公众号' % toUser)
                        basic = Basic()
                        info_data = basic.get_user_info(toUser)
                        conn = Postgres()
                        data = conn.fetchone("select id from wx_user where openid = '%s'" % info_data.get('openid'))
                        logger.info('查看数据库是否存在该用户信息: %s' % data)
                        if not data:
                            sql = """
                                insert into wx_user (openid, username, sex, image_url, province, city, score)
                                values ('%s', '%s', %d, '%s', '%s', '%s', 15);
                            """ % (
                                info_data.get('openid'), info_data.get('nickname'), info_data.get('sex'),
                                info_data.get('headimgurl'), info_data.get('province'), info_data.get('city')
                            )
                            end_time = datetime.strftime(datetime.now() + timedelta(days=7), '%Y-%m-%d')
                            sql += """
                                        insert into wx_user_discount_rel (openid, discount_id, end_time)
                                        values ('%s', %d, '%s');
                                    """ % (info_data.get('openid'), 1, end_time)
                            conn.execute(sql)
                        else:
                            sql = "update wx_user set subscribe = true where openid = '%s'" % toUser
                            conn.execute(sql)

                        content = '您好，欢迎关注密语君^_^\n更多优惠请留意粉丝福利！'
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        self.write(replyMsg.send())
                    # 取消关注公众号事件
                    elif recMsg.Event == 'unsubscribe':
                        logger.info('%s 取消关注公众号' % toUser)
                        conn = Postgres()
                        sql = "update wx_user set subscribe = false where openid = '%s'" % toUser
                        conn.execute(sql)
                    # 菜单点击事件
                    elif recMsg.Event == 'CLICK':
                        eventKey = recMsg.EventKey
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
                    logger.info('recMsg不属于receive.Msg')
                    self.write(reply.Msg().send())
        except Exception as err:
            return err
