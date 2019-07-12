from datetime import datetime, timedelta

from tornado.web import RequestHandler

from wxConfig import APPID, APPSECRET
from common.postgresql_conn import Postgres
from common.log_print import logger
from wx.user_auth import UserAuth


class DiscountHandler(RequestHandler):
    def get(self):
        code = self.get_argument('code', None)
        logger.info('code: %s' % code)

        try:
            user_auth = UserAuth(APPID, APPSECRET, code)
            access_token, openid = user_auth.get_access_token()
        except Exception as e:
            return self.write(str(e))

        # openid = 'oBNuy57qwhveTXWFIrn1n2B5W-k0'

        conn = Postgres()
        sql = """
            select wd.id,name,type,discount,score,count,rule
            from wx_discount as wd
            inner join wx_discount_type as wdt on wd.type_id = wdt.id
            where state = true
            order by id
        """
        data = conn.fetchall(sql)

        return self.render('discount.html', data=data, openid=openid)

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
        if len(count):
            res['code'] = -1
            res['msg'] = '每种类型优惠券只能领取一张，请使用后再领取！'
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
