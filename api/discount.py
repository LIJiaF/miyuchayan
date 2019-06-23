import json
from urllib import request
from datetime import datetime, timedelta

from tornado.web import RequestHandler

from wxConfig import APPID, APPSECRET
from common.postgresqlConn import Postgres
from common.log_print import logger
from common.wrapper_func import wrapper_allow_origin_func

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
        sql = """
            select * 
            from wx_user_discount_rel 
            where discount_id = %d
            and openid = '%s'
            and state = false
        """ % (int(discount_id), openid)
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