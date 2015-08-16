# coding=gbk
from worm import Worm
import os

class GanJiWorm(Worm):
    def process_url(self, url):
        if url.endswith('/'):
            url = 'http://xuzhou.ganji.com' + url
        return url

    def write_to_stdout(self, row):
        pass

    def setup(self):
        os.system('cls')
        print '********************************************************************************'
        print '    欢迎使用赶集网黄页爬虫(www.ganji.com/huangye 作者：Allen 版本：V1.1)         \n'
        print '********************************************************************************'


def main():
    worm = GanJiWorm()
    worm.run()


if __name__ == '__main__':
    main()