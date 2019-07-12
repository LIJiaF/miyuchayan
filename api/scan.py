from datetime import datetime
from io import BytesIO

from tornado.web import RequestHandler

from common.postgresql_conn import Postgres
from common.log_print import logger
from common.qrcode_func import QrcodeFunc
from wx.basic import Basic
from wx.sign import Sign
from wxConfig import APPID


class signatureHandler(RequestHandler):
    def get(self):
        url = self.get_argument('fullUrl', None)
        jsapi_ticket = Basic().get_jsapi_ticket()
        logger.info('url：%s' % url)
        logger.info('jsapi_ticket：%s' % jsapi_ticket)

        sign = Sign(jsapi_ticket, url)
        res = sign.sign()
        res['appid'] = APPID
        logger.info('res：%s' % res)

        return self.finish(res)


class ScanHandler(RequestHandler):
    def get(self):
        openid = self.get_argument('openid', None)
        discount_id = self.get_argument('discount_id', '0')
        logger.info('openid: %s' % openid)
        logger.info('discount_id: %s' % discount_id)

        sql = """
            select openid, discount_id, discount, name, type, rule
            from wx_user_discount_rel as wudr
            inner join wx_discount as wd on wd.id = wudr.discount_id
            inner join wx_discount_type as wdt on wdt.id = wd.type_id
            where openid = '%s'
            and discount_id = %d
            and wudr.state = false
        """ % (openid, int(discount_id))

        res = {
            'code': 0
        }

        conn = Postgres()
        data = conn.fetchone(sql)
        if data:
            res['msg'] = '扫码成功'
            res['data'] = data
        else:
            res['code'] = -1
            res['msg'] = '该优惠券已失效，请勿重复扫码！'

        return self.finish(res)

    def post(self):
        openid = self.get_argument('openid', None)
        discount_id = self.get_argument('discount_id', None)

        use_time = datetime.strftime(datetime.now(), '%Y-%m-%d')

        conn = Postgres()
        sql = """
            update wx_user_discount_rel
            set state = true, use_time = '%s'
            where openid = '%s'
            and discount_id = %d;
        """ % (use_time, openid, int(discount_id))
        sql += """
            update wx_user
            set score = score + 20, experience = experience + 20
            where openid = '%s';
        """ % openid

        res = {
            'code': 0,
        }
        try:
            conn.execute(sql)
            res['msg'] = '使用成功！'
        except Exception:
            res['code'] = -1
            res['msg'] = '使用失败，请重新扫码！'

        return self.finish(res)


class CodeHandler(RequestHandler):
    def get(self):
        content = self.get_argument('content')
        qrcode = QrcodeFunc(content)
        img = qrcode.show()
        msstream = BytesIO()
        img.save(msstream, 'jpeg')
        self.set_header('Content-Type', 'image/jpg')
        self.write(msstream.getvalue())
