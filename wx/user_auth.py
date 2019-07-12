import json
from urllib import request

from common.log_print import logger


class UserAuth(object):
    def __init__(self, appid, appsecret, code):
        self.appid = appid
        self.appsecret = appsecret
        self.code = code

    # 检查access_token是否有效
    def check_access_token(self, access_token, openid):
        check_token_url = 'https://api.weixin.qq.com/sns/auth?access_token=%s&openid=%s' % (access_token, openid)
        chekc_token_data = json.loads(request.urlopen(url=check_token_url).read())
        if chekc_token_data.get('errcode'):
            logger.info('access_token失效')
            return False
        return True

    # 获取access_token
    def get_access_token(self):
        get_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
            self.appid, self.appsecret, self.code)
        token_data = json.loads(request.urlopen(url=get_token_url).read().decode('utf-8'))

        if token_data.get('errcode'):
            logger.error('errcode: %s' % token_data['errcode'])
            logger.error('errmsg: %s' % token_data['errmsg'])
            raise Exception('获取access_token失败，请在微信客户端打开！')

        access_token = token_data.get('access_token', None)
        openid = token_data.get('openid', None)
        refresh_token = token_data.get('refresh_token', None)
        logger.info('access_token: %s', access_token)
        logger.info('openid: %s', openid)
        logger.info('refresh_token: %s', refresh_token)

        if not self.check_access_token():
            refresh_token_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s' % (
                self.appid, refresh_token)
            refresh_data = json.loads(request.urlopen(url=refresh_token_url).read())
            if not refresh_data.get('errcode'):
                logger.info('重新获取access_token、openid')
                access_token = refresh_data.get('access_token', None)
                openid = refresh_data.get('openid', None)
                logger.info('access_token: %s', access_token)
                logger.info('openid: %s', openid)

        return access_token, openid
