# coding=gbk
import time

'''
页面设置
'''
PAGES_AND_PAGE_CODE = (
    'http://xuzhou.ganji.com/zhiyepeixun/o2/',  # 第二页
    'http://xuzhou.ganji.com/zhiyepeixun/o3/',  # 第三页
    1,  # 从第1页开始收集
    30,  # 到第2页结束
)


'''
xpath规则设置
'''
URL_REG = '//*/a[@class="list-info-title"]/@href'  # 提取每页中的url，此url打开后包含公司信息

INFO_REG = {
    'title': '//*/div[@class="title"]/h1/text()',  # 提取标题信息
    'phone': '//*/span[@class="basic-tell-no fc-org"]/text()',  # 提取电话号码
    'person': '//*/div[@class="basic-tell-col clearfix"]/span[@class="fl"]/text()',  # 提取地址
}


'''
编码设置
'''
ENCODING = 'utf-8'


'''
缓存文件设置
'''
USE_LOCAL_URLS = False  # 使用本地缓存的url
URL_FILENAME = time.strftime('%Y-%m-%d') + 'urls.txt'  # 缓存url文件名称


'''
采集信息文件设置
'''
APPEND = False  # 采集到的信息以追加的形式保存
SAVE_FILENAME = 'info'  # 采集到的信息保存到 info.csv 文件中
FILE_HEADER = ['标题', '电话', '联系人']  # 文件头
FILE_HEADER_NAME = ['title', 'phone', 'person']  # 保存顺序


