import xml.etree.ElementTree as ET


def parse_xml(web_data):
    if len(web_data) == 0:
        return None

    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    elif msg_type == 'event':
        event = xmlData.find('Event').text
        if event == 'subscribe':
            return Subscribe(xmlData)
        elif event == 'CLICK':
            return ClickMsg(xmlData)


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text


# 处理文本信息
class TextMsg(Msg):
    def __init__(self, xmlData):
        super(TextMsg, self).__init__(xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")
        self.MsgId = xmlData.find('MsgId').text


# 处理图片信息
class ImageMsg(Msg):
    def __init__(self, xmlData):
        super(ImageMsg, self).__init__(xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text
        self.MsgId = xmlData.find('MsgId').text


# 处理关注事件信息
class Subscribe(Msg):
    def __init__(self, xmlData):
        super(Subscribe, self).__init__(xmlData)
        self.Event = xmlData.find('Event').text


# 处理点击事件信息
class ClickMsg(Msg):
    def __init__(self, xmlData):
        super(ClickMsg, self).__init__(xmlData)
        self.Event = xmlData.find('Event').text
        self.EventKey = xmlData.find('EventKey').text
