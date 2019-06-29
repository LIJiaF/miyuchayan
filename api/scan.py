import json
from urllib import request
from datetime import datetime, timedelta

from tornado.web import RequestHandler

from wxConfig import APPID, APPSECRET
from common.postgresqlConn import Postgres
from common.log_print import logger
from common.wrapper_func import wrapper_allow_origin_func


class ScanHandler(RequestHandler):
    def get(self):
        openid = self.get_argument('openid', None)
        discount_id = self.get_argument('discount_id', None)
        logger.info('openid：%s' % openid)
        logger.info('discount_id：%s' % discount_id)

    @wrapper_allow_origin_func
    def post(self):
        pass
