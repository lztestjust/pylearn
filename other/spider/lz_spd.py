from urllib import request
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import pickle
import json
import re
from queue import Queue
import threading
import subprocess


def load_page():
    # url = r'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
    url = r'http://www.dianping.com/shenzhen/ch30/g136'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    # req = request.Request(url, headers=headers, method='PUT')
    req = request.Request(url, headers=headers)
    # req = request.Request(url, headers=headers)
    # req.get_method = lambda : 'PUT'
    request.build_opener()
    res = request.urlopen(req)
    print(res.read().decode())


def load_page_by_se():
    """加载页面

    使用 selenium 插件
    """
    url = r'https://www.zhihu.com/signin'
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
    driver.get(url)
    acc_xp = '//div[@class="SignFlow-accountInput Input-wrapper"]/input'
    pwd_xp = '//div[@class="SignFlow-password"]/div[1]/div[1]/input'
    btn_xp = '//form[@class="SignFlow"]/button'
    driver.find_element_by_xpath(acc_xp).send_keys('16620990886')
    driver.find_element_by_xpath(pwd_xp).send_keys('zh126355')
    driver.find_element_by_css_selector('.Button.SignFlow-submitButton').click()
    sleep(3)
    driver.find_element_by_css_selector('.Button.SignFlow-submitButton').click()
    # text = captcha()
    # if text:
    #     pass
    #     driver.find_element_by_xpath(btn_xp).submit()
    # try:
    #     cap_xp = '//div[@class="Captcha SignFlow-captchaContainer"]//input'
    #     text = captcha()
    #     driver.find_element_by_xpath(cap_xp).send_keys(text)
    #     driver.find_element_by_xpath(btn_xp).click()
    # except:
    #     print('未找到验证码输入框')
    sleep(5)
    cookies = driver.get_cookies()
    for i in cookies:
        print(i['name'], i['value'])
    sleep(20)
    driver.close()
    driver.quit()


def captcha():
    text = input('请输入验证码：')
    return text


def remote_chrome():
    """调控 chrome 浏览器

    1、使用调控模式打开浏览器
    2、selenium 接管浏览器
    3、实现登录并保存cookie到文件中
    4、关闭 selenium
    """

    cmd_str = 'chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"'
    subprocess.Popen(cmd_str)

    options = Options()
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver',
                             options=options)
    zhihu(driver)


def zhihu(driver):
    """爬取知乎"""
    # print(driver.title)
    url = r'https://www.zhihu.com/signin'
    driver.get(url)
    if driver.title.strip() != '首页 - 知乎':
        acc_xp = '//div[@class="SignFlow-accountInput Input-wrapper"]/input'
        pwd_xp = '//div[@class="SignFlow-password"]/div[1]/div[1]/input'
        btn_xp = '//form[@class="SignFlow"]/button'
        driver.find_element_by_xpath(acc_xp).send_keys('16620990886')
        driver.find_element_by_xpath(pwd_xp).send_keys('zh126355')
        driver.find_element_by_css_selector('.Button.SignFlow-submitButton').click()
        # 保存 cookie 以便使用
        cookie_file = 'cookie.zhihu'
        cookie_dict = {}
        sleep(5)
        cookies = driver.get_cookies()
        for i in cookies:
            cookie_dict[i['name']] = i['value']
        f = open(cookie_file, 'wb')
        pickle.dump(cookie_dict, f)
        f.close()
        # 关闭调控
        sleep(5)
    driver.close()
    driver.quit()


def person_menu(url: str=None):
    """个人主页"""
    if url is None:
        url = 'https://www.zhihu.com/people/lzzhihu/activities'

    cookies = get_cookie_from_file()
    cookies = dict2str(cookies)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'cookie': cookies
    }
    req = request.Request(url, headers=headers)
    res = request.urlopen(req)

    # 获取动态
    response = res.read().decode()
    pattern_str = '<a class="TopicLink" href="//(.*?)" target="_blank">'
    pattern = re.compile(pattern_str, re.S)
    urls = pattern.findall(response)
    print(set(urls))


def topic(url: str=None):
    """记录主题下的文章链接及标题"""

    if not url:
        return

    #
    cookies = get_cookie_from_file()
    cookies = dict2str(cookies)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'cookie': cookies
    }
    req = request.Request(url, headers=headers)
    res = request.urlopen(req)

    # 获取动态
    response = res.read().decode()

    #
    pattern_html = '<div class="List-item TopicFeedItem".*?>(.*?)</div>'
    # url
    pattern_str = '<a.*?href="(/question.*?|//zhuanlan.*?)".*?>'
    # 标题
    pattern_str2 = '<h2 class="ContentItem-title">.*?<a.*?>(.*?)</a>'

    pattern = re.compile(pattern_str, re.S)
    urls = pattern.findall(response)
    data_l = []
    for i in urls:
        print(i)
        if not i.startswith('//'):
            data_l.append('www.zhihu.com' + i)
        else:
            data_l.append(i)

    pattern = re.compile(pattern_str2, re.S)
    title = pattern.findall(response)
    data_ll = []
    for i in title:
        print(i)
        data_ll.append(i)

    data_m = {}
    for i, j in zip(data_l, data_ll):
        data_m.setdefault(len(data_m), [i, j])

    file_path = 'topic.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_m, f)


def topic_by_api(url: str=None):
    """获取主题下的文章链接及标题"""
    if not url:
        return

    # 请求头
    cookies = get_cookie_from_file()
    cookies = dict2str(cookies)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'cookie': cookies
    }
    # 5229.15065
    # 5226.76884 3 -61819
    # 5224.82520 2 005636
    # 5210.84815
    page_queue = Queue()
    ll = []
    for i in range(5209, 5229 + 2, 2):
        ll.append(i)
    ll.reverse()
    for i in ll:
        print(i)
        page_queue.put(i)

    # for j in range(page_queue.qsize()):
    for j in range(len(ll) + 0):
        # url_ = url + '{}{}{}'
        # 请求数据
        # data = {
        #     'include': 'data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;',
        #     'limit': 5,
        #     'after_id': 5210.84815
        # }
        # data = bytes(json.dumps(data), encoding='utf-8')
        include = 'include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;'
        limit = '&limit=' + str(5)
        if not j:
            after_id = ''
        else:
            after_id = '&after_id=' + str(page_queue.get()) + '.00000'
        # after_id = '&after_id=' + str(page_queue.get()) + '.89814'
        # after_id = '&after_id=' + str(page_queue.get()) + '.' + str(randint(10000, 99999))
        # full_url = url_.format(include, limit, after_id)
        full_url = url + include + limit + after_id
        print(full_url)
        req = request.Request(full_url, headers=headers)
        res = request.urlopen(req)
        json_str = res.read().decode()
        # for k, v in json.loads(json_).items():
        #     print(k, v)
        json_ = json.loads(json_str)
        data_ = json_['data']
        file_path = 'topic.txt'
        data_m = {'title': None, 'url': None}
        for i in data_:
            print(i['target'].get('question'))
            # 判断是否为 问题文章
            if i['target'].get('question'):
                # 文章的 title
                data_m['title'] = i['target']['question']['title']
                # 文章的 url
                data_m['url'] = i['target']['question']['url']
            else:
                # 文章的 title
                data_m['title'] = i['target']['title']
                # 文章的 url
                data_m['url'] = i['target']['url']
            # with open(file_path, 'a') as f:
            #     json.dump(data_m, f)
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data_m))
                f.write('\n')
        sleep(5)


class CrawThread(threading.Thread):
    """采集线程"""
    def __init__(self, crawqeue):
        super(CrawThread, self).__init__()
        self.crawqeue = crawqeue

    def run(self):
        global CRAWLQEUE
        global URLQEUE
        while not CRAWLQEUE.empty():
            # 访问地址获取数据
            req = request.Request(self.crawqeue.get(), headers=HEADERS)
            res = request.urlopen(req)
            json_str = res.read().decode()
            json_ = json.loads(json_str)
            data_ = json_['data']
            file_path = 'topic.txt'
            data_m = {'title': None, 'url': None}
            for i in data_:
                print(i['target'].get('question'))
                # 判断是否为 问题文章
                if i['target'].get('question'):
                    # 文章的 title
                    data_m['title'] = i['target']['question']['title']
                    # 文章的 url
                    _url = i['target']['question']['url']
                    _id = i['target']['id']
                    _url = _url.replace('api/v4/', '').replace('questions', 'question') + '/answer/' + str(_id)
                    data_m['url'] = _url
                else:
                    # 文章的 title
                    data_m['title'] = i['target']['title']
                    # 文章的 url
                    data_m['url'] = i['target']['url']

                #
                if data_m['url'] not in URLQEUE:
                    URLQEUE.add(data_m['url'])
                    # 写入文件
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(data_m))
                        f.write('\n')


def topic_by_thread(url: str=None):
    """多线程采集"""
    if not url:
        return

    page_queue = Queue()
    global CRAWLQEUE
    ll = []
    for i in range(5000, 5229 + 5, 5):
        ll.append(i)
    ll.reverse()
    for i in ll:
        print(i)
        page_queue.put(i)
    for j in range(len(ll) + 0):
        include = 'include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;'
        limit = '&limit=' + str(5)
        if not j:
            after_id = ''
        else:
            after_id = '&after_id=' + str(page_queue.get()) + '.00000'
        full_url = url + include + limit + after_id
        CRAWLQEUE.put(full_url)

    # for i in range(CRAWLQEUE.qsize()):
    #     print(CRAWLQEUE.get())
    # 创建三个采集线程
    for i in range(3):
        th = CrawThread(CRAWLQEUE)
        th.start()


def menu_switch(url: str=None):
    """首页 下拉加载

    首页的 推荐 模块在下拉页面自动加载数据
    """
    if not url:
        url = 'https://www.zhihu.com/'

    cmd_str = 'chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"'
    subprocess.Popen(cmd_str)

    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver',
                              options=options)

    driver.get(url)
    sleep(0.8)
    #
    # topstoryitem_lst = '//div[contains(@class, "TopstoryItem-isRecommend")]'
    # topstoryitem_lst = '//h2[contains(@class, "ContentItem-title")]'
    topstoryitem_title_lst = '//h2[@class="ContentItem-title"]'
    topstoryitem_url_lst = '//h2[@class="ContentItem-title"]//a'
    topstoryitem_zan_lst = '//button[contains(@class, "VoteButton--up")]'
    topstoryitem_com_lst = '//div[@class="ContentItem-actions"]/button[1]'
    temp = 10
    temp_len = 0
    while temp:
        print('--------------------------------')
        els = driver.find_elements_by_xpath(topstoryitem_title_lst)
        els2 = driver.find_elements_by_xpath(topstoryitem_url_lst)
        els3 = driver.find_elements_by_xpath(topstoryitem_zan_lst)
        els4 = driver.find_elements_by_xpath(topstoryitem_com_lst)
        zip_obj = zip(els[temp_len:], els2[temp_len:], els3[temp_len:], els4[temp_len:])
        for i, j, k, l in zip_obj:
            print(i.text)
            # j = 'https' + j if j.get_attribute('href').startswith('//') else 'https://www.zhizhu.com' + j.get_attribute('href')
            print(j.get_attribute('href'))
            print(k.text)
            print(l.text)
            # print(i.find_element_by_xpath('//h2').text)
        driver.execute_script('document.documentElement.scrollTop=100000')
        sleep(5)
        temp -= 1
        temp_len = len(els)

    sleep(20)
    driver.close()
    driver.quit()


# 辅助工具
def get_cookie_from_file():
    """从文件中获取cookie"""
    cookie_file = 'cookie.zhihu'
    with open(cookie_file, 'rb') as f:
        data_m = pickle.load(f)
    return data_m


def dict2str(dt: dict=None):
    """字典转字符串"""
    result = ''
    for k, v in dt.items():
        result += k
        result += '='
        result += v
        result += ';'

    return result


# 测试
def __test():
    file_path = r'C:\Users\lztes\Desktop\1.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # # 问题
    # pattern_str = '<a.*?href="(/question.*?)">'
    # # 专栏
    # pattern_str = '<a.*?href="(//zhuanlan.*?)".*?>'
    # 专栏
    pattern_str = '<a.*?href="(/question.*?|//zhuanlan.*?)".*?>'
    # # 标题
    # pattern_str = '<h2 class="ContentItem-title">.*?<a.*?>(.*?)</a>'
    pattern = re.compile(pattern_str, re.S)
    urls = pattern.findall(html)
    for i in urls:
        # print(i)
        if not i.startswith('//'):
            print('www.zhihu.com' + i)


# 常量
COOKIES = get_cookie_from_file()
COOKIES_STR = dict2str(COOKIES)
HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'cookie': COOKIES_STR
    }
CRAWLQEUE = Queue()
URLQEUE = set()


if __name__ == '__main__':
    # 加载页面
    load_page()
    # print(help(request.urlopen))
    # print(help(urllib3.PoolManager))
    # load_page_by_se()

    # # 登录知乎
    # remote_chrome()

    # # 个人主页
    # person_menu()

    # print(type(get_cookie_from_file()))
    # # print(json.dumps(get_cookie_from_file()))
    # for k, v in get_cookie_from_file().items():
    #     # print(k)
    #     print(k +'='+ v + ';')

    # print(dict2str(get_cookie_from_file()))

    # response = '<a class="TopicLink" href="//www.zhihu.com/topic/19556498" target="_blank"><div class="Popover"><div id="null-toggle" aria-haspopup="true" aria-expanded="false" aria-owns="null-content"><img class="Avatar Avatar--large TopicLink-avatar" width="60" height="60" src="https://pic3.zhimg.com/50/ea27f2890_im.jpg" srcSet="https://pic3.zhimg.com/50/ea27f2890_xl.jpg 2x" alt="信息技术（IT）"/></div></div></a></div><div class="ContentItem-head"><h2 class="ContentItem-title"><a class="TopicLink" href="//www.zhihu.com/topic/19556498" target="_blank">'
    # pattern_str = '<a class="TopicLink" href="//(.*?)" target="_blank">'
    # pattern = re.compile(pattern_str, re.S)
    # urls = pattern.findall(response)
    # print(urls)

    # __test()

    # topic('https://www.zhihu.com/topic/19556498')

    # #
    # topic_by_api('https://www.zhihu.com/api/v4/topics/19556498/feeds/top_activity?')

    # #
    # topic_by_thread('https://www.zhihu.com/api/v4/topics/19556498/feeds/top_activity?')

    # print('https://www.zhihu.com/api/v4/questions/47435460'.replace('api/v4/', '').replace('questions', 'question') + '/answer/' + '595908397' )

    # # 首页推荐列表
    # menu_switch()