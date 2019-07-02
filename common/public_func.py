import hashlib


def format_md5(str):
    str_md5 = hashlib.md5(str.encode('utf-8')).hexdigest()
    return str_md5


if __name__ == '__main__':
    str = 'miyuchayan'
    print(format_md5(str))
