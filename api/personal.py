from datetime import datetime, timedelta

from tornado.web import RequestHandler

from wxConfig import APPID, APPSECRET
from common.postgresql_conn import Postgres
from common.log_print import logger
from wx.user_auth import UserAuth


class PersonalHandler(RequestHandler):
    def get(self):
        # 根据code获取网页access_token和openid
        code = self.get_argument('code', None)
        logger.info('code: %s' % code)

        try:
            user_auth = UserAuth(APPID, APPSECRET, code)
            info_data = user_auth.get_user_info()
        except Exception as e:
            return self.write(str(e))

        # openid = 'oBNuy57qwhveTXWFIrn1n2B5W-k0'

        conn = Postgres()
        data = conn.fetchone("select id from wx_user where openid = '%s'" % info_data.get('openid'))
        logger.info('查看数据库是否存在该用户信息: %s' % data)
        if not data:
            sql = """
                insert into wx_user (openid, username, sex, image_url, province, city)
                values ('%s', '%s', %d, '%s', '%s', '%s');
            """ % (
                info_data.get('openid'), info_data.get('nickname'), info_data.get('sex'), info_data.get('headimgurl'),
                info_data.get('province'), info_data.get('city')
            )
            end_time = datetime.strftime(datetime.now() + timedelta(days=7), '%Y-%m-%d')
            sql += """
                insert into wx_user_discount_rel (openid, discount_id, end_time)
                values ('%s', %d, '%s');
            """ % (info_data.get('openid'), 1, end_time)
            conn.execute(sql)
        else:
            sql = """
                update wx_user
                set username = '%s', sex = %d, image_url = '%s', province = '%s', city = '%s'
                where openid = '%s'
            """ % (
                info_data.get('nickname'), info_data.get('sex'), info_data.get('headimgurl'), info_data.get('province'),
                info_data.get('city'), info_data.get('openid')
            )
            conn.execute(sql)

        user_sql = """
            select openid, username, image_url, province, city, score, experience, is_admin, date
            from wx_user 
            where openid = '%s'
        """ % info_data.get('openid')
        user_data = conn.fetchone(user_sql)

        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        discount_sql = """
            select wd.id,discount,name,end_time,type,rule
            from wx_user_discount_rel as wud
            left join wx_discount as wd on wd.id = wud.discount_id
            inner join wx_discount_type as wdt on wdt.id = wd.type_id
            where openid = '%s' 
            and end_time >= '%s'
            and wud.state = false
            order by id desc
        """ % (info_data.get('openid'), now)
        discount_data = conn.fetchall(discount_sql)

        info = {
            'openid': user_data['openid'],
            'username': user_data['username'] or '密语君',
            'province': user_data['province'] or '保密',
            'city': user_data['city'] or '保密',
            'image_url': user_data['image_url'],
            'score': user_data['score'],
            'experience': user_data['experience'],
            'is_admin': user_data['is_admin'],
            'discount': len(discount_data),
            'discount_list': discount_data,
            'is_receive': user_data['date'] >= datetime.strftime(datetime.now(), '%Y-%m-%d')
        }
        logger.info('用户信息: %s' % info)

        return self.render('personal.html', info=info)

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
            conn.execute(
                "update wx_user set score = score + 5, experience = experience + 5, date = '%s' where openid = '%s'" % (
                    now, openid))
            res['msg'] = '积分领取成功'
            return self.finish(res)

        res['code'] = -1
        res['msg'] = '积分领取失败'
        return self.finish(res)
