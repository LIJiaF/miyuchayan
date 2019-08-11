import json
from urllib import request

from wx.basic import Basic
from wxConfig import DISCOUNT_ID, PERSONAL_ID, APPID


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
    basic = Basic()
    accessToken = basic.get_access_token()

    discount_url = request.quote(DISCOUNT_ID)
    discount_callable_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect" % (
        APPID, discount_url)
    personal_url = request.quote(PERSONAL_ID)
    personal_callable_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=123&connect_redirect=1#wechat_redirect" % (
        APPID, personal_url)

    media_id = '4UMCmoF8b-7xciCXzcmFgin-JYiNQkyO7P8XGZ9PZlA'

    postJson = """
    {
        "button":
        [
            {
                "name": "菜单",
                "sub_button": [
                    {
                       "type": "media_id", 
                       "name": "点餐菜单", 
                       "media_id": "%s"
                    },
                    {
                       "type": "click", 
                       "name": "外卖电话", 
                       "key": "phone"
                    },
                    {
                       "type":"click",
                       "name":"积分说明",
                       "key":"score_rule"
                    }
                ]
            },
            {
                "type": "view",
                "name": "粉丝福利",
                "url": "%s"
            },
            {
                "type": "view",
                "name": "个人中心", 
                "url": "%s"
            }
          ]
    }
    """ % (media_id, discount_callable_url, personal_callable_url)

    myMenu = Menu()
    myMenu.create(postJson, accessToken)
