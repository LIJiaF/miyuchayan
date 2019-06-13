import json
from urllib import request
from redis import StrictRedis

APPID = "wx4ad79b44d68db8da"
APPSECRET = "75b8b1f237c468b41124033ba7a05c4a"

redisConfig = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': ''
}

redis = StrictRedis(**redisConfig)


class Basic(object):
    def __init__(self):
        self._accessToken = ''

    def get_access_token(self):
        if not redis.exists('access_token'):
            postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                APPID, APPSECRET))
            urlResp = request.urlopen(postUrl)
            urlResp = json.loads(urlResp.read().decode('utf-8'))

            redis.set('access_token', urlResp['access_token'])
            redis.expire('access_token', 7000)
            self._accessToken = urlResp['access_token']
        else:
            self._accessToken = redis.get('access_token').decode('utf-8')

        return self._accessToken


if __name__ == '__main__':
    basic = Basic()
    basic.get_access_token()
    print('access token 获取成功')
