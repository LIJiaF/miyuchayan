import qrcode


class QrcodeFunc(object):
    def __init__(self, content='LiJiaF'):
        self.content = content
        self.img = None

    def draw(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2
        )
        qr.add_data(self.content)
        qr.make(fit=True)
        img = qr.make_image()

        self.img = img

    def show(self):
        self.draw()
        return self.img

    def save(self, filename='qrcode.png'):
        self.draw()
        filepath = '../static/' + filename
        self.img.save(filepath)


if __name__ == '__main__':
    code = QrcodeFunc()
    code.save()
