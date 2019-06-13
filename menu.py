from urllib import request

from basic import Basic


class Menu(object):
    def __init__(self):
        pass

    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        postData = postData.encode('utf-8')
        urlResp = request.urlopen(url=postUrl, data=postData)
        print(urlResp.read())
        print('菜单添加成功')

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
                "url": "http://www.baidu.com"
            },
            {
                "type": "click",
                "name": "个人中心", 
                "key": "personal"
            }
          ]
    }
    """
    accessToken = Basic().get_access_token()
    myMenu.create(postJson, accessToken)
