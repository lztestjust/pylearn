import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


def open_chrome():
    cmd_str = 'chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"'
    subprocess.Popen(cmd_str)
    # pp.wait()
    # print(pp.stdout.readlines())
    # os.system(cmd_str)
    # os.popen(cmd_str)

    #
    options = Options()
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver',
                              options=options)
    driver.get('https://www.baidu.com/')
    txt = input('请输入任意字符结束应用：')
    if txt:
        driver.close()
        driver.quit()

    # driver.get('https://www.zhihu.com/signin')
    # sleep(5)
    # acc_xp = '//div[@class="SignFlow-accountInput Input-wrapper"]/input'
    # pwd_xp = '//div[@class="SignFlow-password"]/div[1]/div[1]/input'
    # btn_xp = '//form[@class="SignFlow"]/button'
    # driver.find_element_by_xpath(acc_xp).send_keys('16620990886')
    # driver.find_element_by_xpath(pwd_xp).send_keys('zh126355')
    # driver.find_element_by_xpath(btn_xp).click()
    # sleep(30)
    # driver.close()
    # driver.quit()


if __name__ == '__main__':
    # print(help(os.popen))
    # cmd_str = 'dir'
    # pp = os.popen(cmd_str)
    # print(pp.read())
    # 无返回值
    # cmd_str = 'ipconfig'
    # os.system(cmd_str)

    # pp = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)
    # pp.wait()
    # for i in pp.stdout.readlines():
    #     print(i.strip().decode('gbk'))

    open_chrome()