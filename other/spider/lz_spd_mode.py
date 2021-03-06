from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
from time import sleep
import datetime
import time
import os
from random import choice

CUR_DIR = os.curdir


def remote_chrome():
    """调控 chrome 浏览器
    使用调控模式启动浏览器，并返回 webdriver 对象
    """

    # 启动浏览器 调试模式
    cmd_str = 'chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\AutomationProfile"'
    subprocess.Popen(cmd_str)

    options = Options()
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver',
                              options=options)
    return driver


def selenium_less_hander():
    """selenium 使用无头浏览器"""
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver', options=options)
    return driver


def dazondianping(driver):
    """大众点评"""
    url = 'http://www.dianping.com/shenzhen/ch30/g136p5'
    driver.get(url)
    try:
        cinema_name_xp = '//div[@class="pic"]//img'
        cinema_img_xp = '//div[@class="pic"]//img/@src'
        star_xp = '//div[@class="txt"]//div[@class="comment"]/span/@title'
        review_xp = '//div[@class="txt"]//div[@class="comment"]/a[1]/b'
        pre_capita_xp = '//div[@class="txt"]//div[@class="comment"]/a[2]/b'
        cinema_addr1_xp = '//div[@class="txt"]//div[@class="tag-addr"]/a[2]/span[@class="tag"]'
        cinema_addr2_xp = '//div[@class="txt"]//div[@class="tag-addr"]//span[@class="addr"]'

        cinema_name = driver.find_elements_by_xpath(cinema_name_xp)
        cinema_addr1 = driver.find_elements_by_xpath(cinema_addr1_xp)
        print('--------------------------')
        for i in cinema_name:
            print(i.get_attribute('title'))
        print('--------------------------')
        for i in cinema_addr1:
            print(i.text)

    except Exception as e:
        print('出现错误')
        print(e)
    finally:
        driver.close()
        driver.quit()


def tuzhan_word():
    # url = r'https://v5.rabbitpre.com/m2/aUe1ZjL54Y'

    urls = ['https://v5.rabbitpre.com/m2/aUe1ZjL54Y',
           'https://v5.rabbitpre.com/m2/aUe1ZjMLP5',
           'https://v5.rabbitpre.com/m2/aUe1ZjML0H',
           'https://v5.rabbitpre.com/m2/aUe1ZjML0D',
           'https://v5.rabbitpre.com/m2/aUe1ZjLWQ1',
           'http://v5.rabbitpre.com/v/amm2Mb7',
           'https://v5.rabbitpre.com/m2/aUe1ZjLGI2',
           'https://v5.rabbitpre.com/m2/aUe1ZjLGIz',
           'https://v5.rabbitpre.com/m2/aUe1ZjLGSS'
           ]
    # urls = ['https://testa2.rabbitpre.com/m2/aUe1Zi90wA', 'https://testa2.rabbitpre.com/m2/aUe1Zi90wc',
    #         'http://testa2.rabbitpre.com/v/eaINZni', 'https://testa2.rabbitpre.com/m2/aUe1Zi90wT',
    #         'https://testa2.rabbitpre.com/m2/aUe1Zi90w4', 'https://testa2.rabbitpre.com/m2/aUe1Zi90wR',
    #         'https://testa2.rabbitpre.com/m2/aUe1Zi90wM', 'https://testa2.rabbitpre.com/m2/aUe1Zi90wa',
    #         'https://testa2.rabbitpre.com/m2/aUe1Zi90w6', 'https://testa2.rabbitpre.com/m2/aUe1Zi90w5']

    driver = remote_chrome()
    try:
        # driver.get(url)
        driver.get(choice(urls))
        sleep(2)
    except:

        fp = str(int(time.time())) + '.png'
        driver.save_screenshot(os.path.join(CUR_DIR, fp))
    finally:
        driver.close()


if __name__ == '__main__':
    # # 调控浏览器
    # driver = remote_chrome()
    #
    # # 大众点评
    # dazondianping(driver)

    # driver_ = selenium_less_hander()
    # url_ = 'http://www.dianping.com/'
    # driver_.get(url_)
    # sleep(1)
    # print(driver_.page_source)
    # data_cookies_m_ = {}
    # cookies_ = driver_.get_cookies()
    # for i in cookies_:
    #     data_cookies_m_[i['name']] = i['value']
    # print(data_cookies_m_)
    # print(CUR_DIR)
    for i in range(100):
        tuzhan_word()
