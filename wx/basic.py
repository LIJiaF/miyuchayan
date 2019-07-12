import json
import os
from urllib import request

from wxConfig import APPID, APPSECRET
from common.redis_conn import redis
from common.log_print import logger


class Basic(object):
    def __init__(self):
        pass

    # 获取access_token
    def get_access_token(self):
        access_token = ''
        if not redis.exists('token:access_token'):
            postUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                APPID, APPSECRET)
            urlResp = request.urlopen(postUrl)
            urlResp = json.loads(urlResp.read().decode('utf-8'))

            if not urlResp.get('errcode'):
                redis.set('token:access_token', urlResp['access_token'])
                redis.expire('token:access_token', 7000)
                access_token = urlResp['access_token']
                logger.info('access_token获取成功')
            else:
                logger.error('access_token获取失败')
                logger.error('errcode: %s' % urlResp['errcode'])
                logger.error('errmsg: %s' % urlResp['errmsg'])
        else:
            access_token = redis.get('token:access_token').decode('utf-8')
            logger.info('access_token获取成功')

        return access_token

    # 获取jsapi_ticket
    def get_jsapi_ticket(self):
        jsapi_ticket = ''
        if not redis.exists('token:jsapi_ticket'):
            access_token = self.get_access_token()
            postUrl = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % access_token
            urlResp = request.urlopen(postUrl)
            urlResp = json.loads(urlResp.read().decode('utf-8'))

            if not urlResp.get('errcode'):
                redis.set('token:jsapi_ticket', urlResp['ticket'])
                redis.expire('token:jsapi_ticket', 7000)
                jsapi_ticket = urlResp['ticket']
                logger.info('jsapi_ticket获取成功')
            else:
                logger.error('jsapi_ticket获取失败')
                logger.error('errcode: %s' % urlResp['errcode'])
                logger.error('errmsg: %s' % urlResp['errmsg'])
        else:
            jsapi_ticket = redis.get('token:jsapi_ticket').decode('utf-8')
            logger.info('jsapi_ticket获取成功')

        return jsapi_ticket

    # 上传永久素材
    def upload_permanently_media(self, type='image'):
        accessToken = self.get_access_token()
        media = os.path.join(os.path.dirname(__file__), 'menu.jpg')
        description = '{"title": "menu", "introduction": "菜单"}'.encode('utf-8')
        cmd = 'curl "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" -F media=@%s -F description=%s' % (
            accessToken, type, media, description)
        print(os.popen(cmd).read())

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
            return urlResp
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
    # basic.upload_permanently_media()
    # basic.get_media_count()
    basic.get_media_list()
