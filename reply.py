import time


class Msg(object):
    def __init__(self):
        pass

    def send(self):
        return "success"


class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self._dict = dict()
        self._dict['ToUserName'] = toUserName
        self._dict['FromUserName'] = fromUserName
        self._dict['CreateTime'] = int(time.time())
        self._dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self._dict)


class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self._dict = dict()
        self._dict['ToUserName'] = toUserName
        self._dict['FromUserName'] = fromUserName
        self._dict['CreateTime'] = int(time.time())
        self._dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self._dict)


class ArticleMsg(Msg):
    def __init__(self, toUserName, fromUserName, title, description, picUrl, url):
        self._dict = dict()
        self._dict['ToUserName'] = toUserName
        self._dict['FromUserName'] = fromUserName
        self._dict['CreateTime'] = int(time.time())
        self._dict['Title'] = title
        self._dict['Description'] = description
        self._dict['PicUrl'] = picUrl
        self._dict['Url'] = url

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[{Title}]]></Title>
        <Description><![CDATA[{Description}]]></Description>
        <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
        <Url><![CDATA[{Url}]]></Url>
        </item>
        </Articles>
        </xml>
        """
        return XmlForm.format(**self._dict)
