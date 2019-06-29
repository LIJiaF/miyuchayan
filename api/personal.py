import json
from urllib import request
from datetime import datetime, timedelta

from tornado.web import RequestHandler

from wxConfig import APPID, APPSECRET
from common.postgresqlConn import Postgres
from common.log_print import logger
from common.wrapper_func import wrapper_allow_origin_func


class PersonalHandler(RequestHandler):
    def get(self):
        # 根据code获取网页access_token和openid
        code = self.get_argument('code', None)
        logger.info('code: %s' % code)
        get_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
            APPID, APPSECRET, code)
        token_data = json.loads(request.urlopen(url=get_token_url).read().decode('utf-8'))
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
        # openid = 'oBNuy57qwhveTXWFIrn1n2B5W-k0'

        user_sql = """
            select openid, username, image_url, province, city, score, experience, is_admin, date
            from wx_user 
            where openid = '%s'
        """ % openid
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
        """ % (openid, now)
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
            conn.execute(
                "update wx_user set score = score + 5, experience = experience + 5, date = '%s' where openid = '%s'" % (
                    now, openid))
            res['msg'] = '积分领取成功'
            return self.finish(res)

        res['code'] = -1
        res['msg'] = '积分领取失败'
        return self.finish(res)
