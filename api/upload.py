import math
import random
import os
from datetime import datetime

from tornado.web import RequestHandler

from wx.basic import Basic
from common.redis_conn import redis

class UploadHandler(RequestHandler):
    def get(self):
        accessToken = Basic().get_access_token()
        return self.render('upload.html', accessToken=accessToken)

    def post(self):
        files = self.request.files.get('img', None)
        if files:
            if not files:
                return self.write('上传图片不能为空')

            upload_path = os.path.join(os.path.dirname(__file__), 'upload')
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)

            for file in files:
                if file['content_type'] not in ['image/png', 'image/jpeg']:
                    return self.write('上传图片格式有误')

                try:
                    name = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + str(math.floor(random.random() * 10))
                    sName = name + '.' + file['filename'].split('.')[1]
                    with open(os.path.join(upload_path, sName), 'wb') as up:
                        up.write(file['body'])

                    accessToken = Basic().get_access_token()
                    cmd = 'curl -F media=@upload/%s "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=%s"' % (
                        sName, accessToken)
                    wxName = json.loads(os.popen(cmd).read())['url']
                    fName = file['filename']

                    redis.hmset('wx:' + name, {'sname': sName, 'wxname': wxName, 'fname': fName})
                except Exception:
                    print(file['filename'] + '文件上传失败')

            return self.write('图片上传成功')
