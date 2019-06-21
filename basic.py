import json
from urllib import request

from wxConfig import APPID, APPSECRET
from common.redisConn import redis
from common.log_print import logger


class Basic(object):
    def __init__(self):
        self._accessToken = ''

    def get_access_token(self, appid, appsecret):
        if not redis.exists('token:access_token'):
            postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                appid, appsecret))
            urlResp = request.urlopen(postUrl)
            urlResp = json.loads(urlResp.read().decode('utf-8'))

            if not urlResp.get('errcode'):
                redis.set('token:access_token', urlResp['access_token'])
                redis.expire('token:access_token', 7000)
                self._accessToken = urlResp['access_token']
                logger.error('access_token获取成功')
            else:
                logger.error('access_token获取失败')
        else:
            self._accessToken = redis.get('token:access_token').decode('utf-8')
            logger.error('access_token获取成功')

        return self._accessToken


if __name__ == '__main__':
    basic = Basic()
    basic.get_access_token(APPID, APPSECRET)
