import json
from urllib import request

from wxConfig import APPID, APPSECRET
from common.redisConn import redis


class Basic(object):
    def __init__(self):
        self._accessToken = ''

    def get_access_token(self):
        if not redis.exists('token:access_token'):
            postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                APPID, APPSECRET))
            urlResp = request.urlopen(postUrl)
            urlResp = json.loads(urlResp.read().decode('utf-8'))

            redis.set('token:access_token', urlResp['access_token'])
            redis.expire('token:access_token', 7000)
            self._accessToken = urlResp['access_token']
        else:
            self._accessToken = redis.get('token:access_token').decode('utf-8')

        return self._accessToken


if __name__ == '__main__':
    basic = Basic()
    basic.get_access_token()
    print('access token 获取成功')
