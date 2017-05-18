# -*- coding: utf-8 -*-
import re
import scrapy
import sys

from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from tutorial.items import ExchangeRateItem


reload(sys)
sys.setdefaultencoding('utf8')


class MySpider(scrapy.Spider):

    name = "spider"
    start_urls = [
        'http://www.pbc.gov.cn/zhengcehuobisi/125207/125217/125925/17105/index1.html'
    ]
    # for i in range(1,31):
    #     start_urls.append("http://www.pbc.gov.cn/zhengcehuobisi/125207/125217/125925/17105/"
    #                       + "index" + str(i)
    #                       + ".html")
    # allowed_domains = ["pbc.gov.cn"]

    name_dict = {'dollar': '美元', 'euro': '欧元', 'yen': '日元', 'hk': '港币',
                 'pound': '英镑', 'australian': '澳大利亚元', 'new_zealand': '新西兰元',
                 'singapore': '新加坡元', 'swiss_franc': '瑞士法郎', 'canada': '加拿大', 'myr': '林吉特',
                 'rub': '俄罗斯卢布', 'zar': '南非兰特', 'south_korean': '韩元',
                 'rahm': '阿联酋迪拉姆', 'sar': '沙特里亚尔'}

    def parse(self, response):
        driver = self.get_firefox_driver()
        # driver.implicitly_wait(30)
        base_url = "http://www.pbc.gov.cn/"
        for index in range(1, 31):
            page_url = base_url + '/zhengcehuobisi/125207/125217/125925/17105/index' \
                       + str(index) + '.html'
            while True:
                driver.get(page_url)
                if '404' not in driver.find_element_by_tag_name('title').text:
                    break
            driver.implicitly_wait(20)
            elements = driver.find_elements_by_class_name('newslist_style')
            # i = 0
            cont_driver = self.get_firefox_driver()
            for element in elements:
                url_content = element.find_element_by_tag_name('a').get_attribute('href')
                content = self.process_url(cont_driver, url_content).encode('utf-8')
                yield self.process_str(content)

                # print '##################'
                # print '美元'.encode('utf-8') in content
                # i += 1
                # if i > 0:
                #     break
            cont_driver.quit()
        driver.quit()

    def process_url(self, cont_driver, url_content):
        driver = cont_driver
        while True:
            driver.get(url_content)
            if 'was not found on this server.' not in driver.find_element_by_tag_name('p').text:
                break

        driver.implicitly_wait(20)
        str_content = driver.find_element_by_id('zoom').find_element_by_tag_name('p').text
        # driver.quit()
        return str_content

    def get_firefox_driver(self):
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        return webdriver.Firefox(capabilities=firefox_capabilities)

        # content = response.css('div#zoom > a::text').extract()
        # f = open('contents')
        # lines = f.readlines()
        # f.close()
        # with open('contents', 'wb') as f:
        #     lines.append(app.py)
        #     f.writelines(lines)

    def process_str(self, content):
        item = ExchangeRateItem()
        # print '####@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2@@@'
        # for key in item.fields.iterkeys():
        #     print key
        # print '###################################################'
        strs = content.split('，')
        # initial item's fields
        for key in item.keys():
            item[key] = float(0)
        # process the content in page
        for st in strs:
            date_group = re.search('\d+年\d+月\d+日', st)
            if date_group:
                item['date'] = date_group.group(0).encode('utf-8')

            for key in item.fields.iterkeys():
                # print '###################'
                # print key
                # print key.encode('utf-8') in self.name_dict
                # print self.name_dict[key]
                if key in self.name_dict and self.name_dict[key] in st:
                    if st.startswith('1'):
                        rmb = re.search(r'\d+\.\d+', st).group(0)
                        foreign = re.search(r'1\d*', st).group(0)
                        item[key] = float(rmb)/float(foreign)
                        if key == 'yen':
                            print '#################'
                            print 'yen:' + foreign
                            print 'rmb:' + rmb
                            print float(rmb)/float(foreign)
                    elif st.startswith('人民币'):
                        foreign = re.search(r'\d+\.?\d+', st).group(0)
                        item[key] = float(1)/float(foreign)
        return item
