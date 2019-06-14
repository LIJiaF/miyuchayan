import json
from urllib import request

from basic import Basic


class Menu(object):
    def __init__(self):
        pass

    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        postData = postData.encode('utf-8')
        urlResp = request.urlopen(url=postUrl, data=postData)
        resData = json.loads(urlResp.read().decode('utf-8'))
        if not resData['errcode']:
            print('菜单添加成功')
        else:
            print('菜单添加失败')
            print('errcode: ', resData['errcode'])
            print('errmsg: ', resData['errmsg'])

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = request.urlopen(url=postUrl)
        print(urlResp.read())

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = request.urlopen(url=postUrl)
        print(urlResp.read())

    # 获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = request.urlopen(url=postUrl)
        print(urlResp.read())


if __name__ == '__main__':
    redirect_uri = request.quote('http://120.76.56.231/discount')
    callable_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx4ad79b44d68db8da&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect" % redirect_uri

    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "click",
                "name": "精彩回顾",
                "key":  "history"
            },
            {
                "type": "view",
                "name": "粉丝福利",
                "url": "%s"
            },
            {
                "type": "click",
                "name": "个人中心", 
                "key": "personal"
            }
          ]
    }
    """ % callable_url
    accessToken = Basic().get_access_token()
    myMenu.create(postJson, accessToken)
