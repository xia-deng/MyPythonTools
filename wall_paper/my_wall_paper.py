# -*- coding: utf-8 -*-
'''
这是一个简单的，旨在自动替换当前的桌面的工具，一个简单的玩意儿
'''
import ctypes
import datetime
import os
from threading import Timer
from urllib import request

# from bs4 import BeautifulSoup


class WallPaperOwner(object):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
    }

    def get_str(self, url):
        response_body = self.__get(url)
        if type(response_body) == bytes:
            return str(response_body, encoding='utf8')
        else:
            return response_body

    def __get(self, url):
        my_request = request.Request(url, headers=self.header)
        response = request.urlopen(my_request)
        response_body = (response.read())
        return response_body

    # 获取最新的壁纸，就是第一条壁纸
    # def fetch_today_paper(self, url, html_body):
    #     soup = BeautifulSoup(html_body, "html.parser")
    #     link_tag_a_list = (soup.find_all("a", class_="mark"))
    #     link = url + link_tag_a_list[0]['href']
    #     soup = BeautifulSoup(self.get_str(link), "html.parser")
    #     return soup.find_all("img", class_="target progressive__img progressive--not-loaded")[0]['data-progressive']

    def save_image(self, link):
        image_response = self.__get(link)
        image_name = str(datetime.date.today()) + '.jpg'
        dir = 'd:/my_images/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        file = dir + image_name
        with open(file, "wb") as f:
            f.write(image_response)  # 将内容写入图片
        return file

    def set_wall_paper(self, file):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, file, 0)


def change_wall_paper():
    print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    pw = WallPaperOwner()
    # link = pw.fetch_today_paper(url, pw.get_str(url))
    file = pw.save_image('https://area.sinaapp.com/bingImg/')
    pw.set_wall_paper(file)
    t = Timer(3600*3, change_wall_paper)
    t.start()


if __name__ == '__main__':
    # url = 'https://bing.ioliu.cn/'
    #pw = WallPaperOwner()
    # link = pw.fetch_today_paper(url, pw.get_str(url))
    #file = pw.save_image('https://area.sinaapp.com/bingImg/')
    #pw.set_wall_paper(file)
    print("the timing task to change wall paper.")
    change_wall_paper()
