import sys
import time
import ddddocr
import requests
from requests.adapters import HTTPAdapter
import http.client
import io
import os
from PIL import Image
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re


ua = UserAgent()
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

headers = {'User-Agent': ua.random,
           'Upgrade-Insecure-Requests': '1',
           'Host': 'www.doki8.net'}

main_url = 'http://www.doki8.net/'
register_url = 'http://www.doki8.net/wp-login.php'
captcha_url = 'http://www.doki8.net/wp-content/plugins/dx-login-register/extends/captcha/captcha.php'
comment_url = 'http://www.doki8.net/wp-comments-post.php'
encoding = 'utf-8'


class Doki8:
    def __init__(self, username, password):
        self.session = requests.session()
        adapter = HTTPAdapter(
            pool_connections=20,
            pool_maxsize=20,
            max_retries=5,
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.login(username, password)

    def get_response(self, url, headers, params=None, proxies=None, encoding='utf-8'):

        try:
            response = self.session.get(url=url, headers=headers,
                                params=params, proxies=proxies, timeout=10)
            response.encoding = encoding
            return response
        except requests.exceptions.RequestException as e:
            print(f'【ERROR】{e}')
            sys.exit()

    def post_response(self,  url, headers, params=None, proxies=None, encoding='utf-8'):
        try:
            response = self.session.post(url=url, data=params,
                                    headers=headers, proxies=proxies, timeout=10)
            response.encoding = encoding
            return response
        except requests.exceptions.RequestException as e:
            print(f'【ERROR】{e}')
            sys.exit()

    @staticmethod
    def byt_to_png(content, path, name):
        byte_stream = io.BytesIO(content)  # 请求数据转化字节流
        roiImg = Image.open(byte_stream)  # Image打开二进制流Byte字节流数据
        imgByteArr = io.BytesIO()  # 创建一个空的Bytes对象
        roiImg.save(imgByteArr, format='PNG')  # PNG就是图片格式
        imgByteArr = imgByteArr.getvalue()  # 保存的二进制流
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + name, "wb+") as f:
            f.write(imgByteArr)

    @staticmethod
    def get_captcha(img_name):
        ocr = ddddocr.DdddOcr()
        with open(img_name, 'rb') as f:
            img_bytes = f.read()
        captcha = ocr.classification(img_bytes)
        return captcha


    @staticmethod
    def bs4_parsing_infos(selector, data):
        bf = BeautifulSoup(data, 'lxml')
        infos = bf.select(selector)
        return infos

    def login(self, username, password):
        try:
            self.get_response(url=register_url, headers=headers)
            content = self.get_response(url=captcha_url, headers=headers).content
            img_name = 'captcha.png'
            Doki8.byt_to_png(content, './', img_name)
            captcha = Doki8.get_captcha(img_name)
            params = {
                "log": f"{username}",
                "pwd": f"{password}",
                "captcha": captcha,
                "rememberme": "forever",
                "wp-submit": "登录"
            }
            response = self.post_response(url=register_url, params=params, headers=headers)
            if '无效的用户名' in response.text:
                print('【ERROR】请检查你的用户名和密码是否正确！！！')
                sys.exit()
            else:
                print('登录成功！！！')
        except Exception as e:
            print(f'【ERROR】{e}')

    def get_integral(self):
        try:
            text = self.get_response(url=main_url, headers=headers).text
            integral = int(re.findall('积分: (\d+) 心动豆', text)[0])
            return text, integral
        except Exception as e:
            print(e)

    @staticmethod
    def get_tv_num(response_text, ls_index):
        href = response_text[ls_index].a['href']
        tv_num = re.findall('(\d+).html', href)[0]
        return tv_num

    def get_comment_response(self, tv_num):
        comment = {
            "comment": "感谢分享",
            "submit": "发表评论",
            "comment_post_ID": tv_num,
            "comment_parent": 0,
        }
        response = self.post_response(url=comment_url, params=comment, headers=headers)
        return response


if __name__ == '__main__':
    user_name = os.environ.get('USER_NAME') if os.environ.get('USER_NAME') else input('请输入登录的用户名：')
    passwd = os.environ.get('PASSWD') if os.environ.get('PASSWD') else input('请输入登录的密码：')
    doki8 = Doki8(user_name, passwd)
    text, old_integral = doki8.get_integral()
    test = doki8.bs4_parsing_infos('div.post-thumbnail', text)
    tv_num = doki8.get_tv_num(test, 0)
    comment_response = doki8.get_comment_response(tv_num).text
    tmp, new_integral = doki8.get_integral()
    if '重复评论' not in comment_response:
        if new_integral != old_integral:
            print(f'经过1次,评论成功的网页：http://www.doki8.net/{tv_num}.html')
        else:
            while new_integral == old_integral:
                for i in range(1, len(test)):
                    tv_num = doki8.get_tv_num(test, i)
                    comment_response = doki8.get_comment_response(tv_num).text
                    time.sleep(1)
                    tmp, new_integral = doki8.get_integral()
                else:
                    print(f'经过{i+1}次，评论成功的网页：http://www.doki8.net/{tv_num}.html')
            print('已完成每日的签到和评论')
    else:
        print('已完成每日的签到和评论请勿重复评论！！！')
