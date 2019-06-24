import json
from urllib import request

from wxConfig import APPID, APPSECRET
from common.redisConn import redis
from common.log_print import logger


class Basic(object):
    def __init__(self):
        self.appid = APPID
        self.appsecret = APPSECRET
        self._accessToken = ''

    # 获取access_token
    def get_access_token(self):
        if not redis.exists('token:access_token'):
            postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                self.appid, self.appsecret))
            urlResp = request.urlopen(postUrl)
            urlResp = json.loads(urlResp.read().decode('utf-8'))

            if not urlResp.get('errcode'):
                redis.set('token:access_token', urlResp['access_token'])
                redis.expire('token:access_token', 7000)
                self._accessToken = urlResp['access_token']
                logger.info('access_token获取成功')
            else:
                logger.error('access_token获取失败')
                logger.error('errcode: %s' % urlResp['errcode'])
                logger.error('errmsg: %s' % urlResp['errmsg'])
        else:
            self._accessToken = redis.get('token:access_token').decode('utf-8')
            logger.info('access_token获取成功')

        return self._accessToken

    # 获取素材列表
    def get_media_list(self, type='image', offset=0, count=10):
        access_token = self.get_access_token()
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % access_token
        postData = {
            'type': type,
            'offset': offset,
            'count': count
        }
        headers = {
            'content-type': 'application/json'
        }
        req = request.Request(url=postUrl, headers=headers, data=json.dumps(postData).encode('utf-8'), method='POST')
        urlResp = json.loads(request.urlopen(req).read().decode('utf-8'))
        if not urlResp.get('errcode'):
            logger.info('media_list获取成功')
            logger.info('media_list: %s' % urlResp)
        else:
            logger.error('media_list获取失败')
            logger.error('errcode: %s' % urlResp['errcode'])
            logger.error('errmsg: %s' % urlResp['errmsg'])

    # 获取素材总数
    def get_media_count(self):
        access_token = self.get_access_token()
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s" % access_token
        urlResp = request.urlopen(url=postUrl)
        urlResp = json.loads(urlResp.read().decode('utf-8'))
        if not urlResp.get('errcode'):
            logger.info('media_count获取成功')
            logger.info('media_count: %s' % urlResp)
        else:
            logger.error('media_count获取失败')
            logger.error('errcode: %s' % urlResp['errcode'])
            logger.error('errmsg: %s' % urlResp['errmsg'])


if __name__ == '__main__':
    basic = Basic()
    # basic.get_access_token()
    # basic.get_media_count()
    basic.get_media_list()
