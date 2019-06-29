import time
import random
import string
import hashlib

from basic import Basic


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self._create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self._create_timestamp(),
            'url': url
        }

    def _create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def _create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string.encode('utf-8')).hexdigest()

        return self.ret


if __name__ == '__main__':
    url = 'http://example.com'
    jsapi_ticket = Basic.get_jsapi_ticket()
    sign = Sign(jsapi_ticket, url)

    print(sign.sign())
