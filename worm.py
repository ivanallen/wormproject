# coding=gbk
import crifanLib
import traceback
import time
import lxml
import re
import json
import csv
import os
import re
from config import *
from multiprocessing import Pool


class Worm(object):

    def get_page(self, page2, page3, pagestart, pageend):
        flag = True
        for index, value in enumerate(page2):
            if value != page3[index]:
                if flag:
                    start = index
                    flag = False
                end = index
        base1 = page2[:start]
        base2 = page3[end+1:]

        pages = [base1+str(i+pagestart)+base2 for i in xrange(pageend-pagestart+1)]
        return pages

    def process_url(self, url):
        return url

    def get_urls_prompt(self):
        print '\n\n'
        print "正在获取urls..."


    def get_urls(self, pages, reg, encoding='utf-8', funcobj=None):
        temp_urls = []
        # pool = Pool(10)
        # args = [(page, reg, encoding) for page in pages]
        # urlss = pool.map(Worm._get_urls, args)
        # for each in urlss:
        #    urls.extend(each)
        total = len(pages)
        self.get_urls_prompt()
        for index, page in enumerate(pages):
            ratio = float(index + 1) / total
            self.draw_progress_bar(ratio)
            temp_urls.extend(self.__get_urls(page, reg, encoding))

        urls = [funcobj(url) for url in temp_urls]
        return urls

    def save_urls_to_local(self, urls, filename):
        with open(filename, 'wb') as f:
            json.dump(urls, f)

    def get_urls_from_local(self, filename):
        with open(filename, 'rb') as f:
            urls = json.load(f)
            return urls

    def __get_urls(self, page, reg, encoding='utf-8'):
        try:
            html = crifanLib.getUrlRespHtml(page)
            selector = lxml.etree.HTML(html)
            urls = selector.xpath(reg)
            return urls
        except:
            date = time.strftime('%Y-%m-%d')
            f = open(date + 'errors.log', 'a')
            hms = time.strftime('%H:%M:%S : \n')
            f.write(hms)
            traceback.print_exc(file=f)
            f.write('\n')
            f.flush()
            f.close()

    def parse(self, url, encoding='utf-8', **kwargs):
        try:
            html = crifanLib.getUrlRespHtml(url)
            selector = lxml.etree.HTML(html)
            results = {}
            for key, value in kwargs.items():
                res = selector.xpath(value)
                for index, value in enumerate(res):
                    data = value
                    if isinstance(data, lxml.etree._Element):
                        data = value.xpath('string(.)')
                    if isinstance(data, unicode):
                        data = data.encode('gbk', 'ignore')
                    data = re.sub('\s', '', data, flags=re.UNICODE)
                    res[index] = data
                results[key] = res
            return results

        except:
            date = time.strftime('%Y-%m-%d')
            f = open(date + 'errors.log', 'a')
            hms = time.strftime('%H:%M:%S : \r\n')
            f.write(hms)
            traceback.print_exc(file=f)
            f.write('\n')
            f.flush()
            f.close()

    def process_result(self, li):
        s = ""
        if li:
            for index, value in enumerate(li):
                value = re.sub(r'\s', '', value)
                if not len(value) == 0:
                    if index == 0:
                        s = "[" + value
                    else:
                        s += ", " + value
            s += "]"
        return s

    def setup(self):
        os.system('cls')

    def run_prompt(self):
        print '\n\n'
        print "正在获取企业资料..."

    def run(self):
        self.setup()
        if not APPEND:
            with open(SAVE_FILENAME + '.csv', 'wb') as csvfile:
                out = csv.writer(csvfile, dialect='excel')
                out.writerow(FILE_HEADER)

        pages = self.get_page(*PAGES_AND_PAGE_CODE)
        if USE_LOCAL_URLS and os.path.exists(URL_FILENAME):
            urls = self.get_urls_from_local(URL_FILENAME)
        else:
            urls = self.get_urls(pages, URL_REG, ENCODING, self.process_url)
            with open(URL_FILENAME, 'wb') as f:
                json.dump(urls, f)

        self.run_prompt()
        total = len(urls)
        for index, url in enumerate(urls):
            try:
                ratio = float(index + 1) / total
                self.draw_progress_bar(ratio)
                info = self.parse(url, **INFO_REG)

                if info:
                    row = [self.process_result(info[v]) for v in FILE_HEADER_NAME]
                    self.write_to_local(row)
                    self.write_to_stdout(row)
            except Exception, e:
                print e

    def write_to_local(self, row):
        with open(SAVE_FILENAME + '.csv', 'ab') as csvfile:
            out = csv.writer(csvfile, dialect='excel')
            out.writerow(row)

    def write_to_stdout(self, row):
        for v in row:
            print v,
        print

    def draw_progress_bar(self, ratio, length=50):
        numequals = int(ratio * length)
        whitespaces = length - numequals
        progress = '【' + '=' * numequals + ' ' * whitespaces + '】 %.2f%%' % (ratio * 100)
        print '\b' * 80,
        print progress,

if __name__ == '__main__':
    worm = Worm()
    worm.run()




