"""
DNF体验服论坛自动签到py
1. 用户输入密码
2. 访问主url
3. 登录QQ
4. 找到签到入口
5. 填写问卷
6. 正式签到
7. 签到成功
"""

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image


class DnfCheck(object):
    def __init__(self, qq_id, qq_pas, option):
        self.qq_id = qq_id
        self.qq_pas = qq_pas
        self.driver = webdriver.Chrome()
        self.url = 'https://dnf.gamebbs.qq.com/forum.php'   # https://wj.qq.com/s2/5321935/e125/
        self.now_time = datetime.datetime.now()
        self.present_time = self.now_time.strftime('%m月%d日')
        self.element = WebDriverWait(self.driver, 10)
        # self.handles = self.driver.window_handles

    def open_browser(self):
        """ 1. 打开浏览器 """
        self.driver.get(self.url)
        self.driver.maximize_window()

    def login_qq(self):
        """ 2. 官方主页登录QQ """
        try:
            self.driver.switch_to.frame("ui_ptlogin")  # 切换框架
            self.element.until(EC.presence_of_element_located((By.ID, 'switcher_plogin')))
            self.driver.find_element_by_id('switcher_plogin').click()  # 点击
            time.sleep(1)
            # 登录QQ
            self.driver.find_element_by_id('u').send_keys(self.qq_id)   # 输入
            self.driver.find_element_by_id('p').send_keys(self.qq_pas)
            time.sleep(1)
            self.driver.find_element_by_id('login_button').click()
        except Exception as e:
            print("未弹窗 无法登录")
            self.driver.save_screenshot("报错图片.png")
            time.sleep(1)
            self.login_qq1()

    def login_qq1(self):
        """ 2-1 未弹窗,主动登录QQ """
        image = Image.open("报错图片.png")
        image.show()

    def button1_click(self):
        """ 3. 点击官网体验服专区 """
        self.element.until(EC.presence_of_element_located((By.ID, 'ax_bk_42')))     # 等待加载
        self.driver.find_element_by_id('ax_bk_42').click()  # 点击体三入口

    def button2_click(self):
        """ 4. 点击体验三区论坛 """
        self.element.until(EC.presence_of_element_located((By.XPATH, '//*[@id="stickthread_1044368"]'
                                                                     '/tr/th/div[2]/div[1]/a')))  # 等待加载
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="stickthread_1044368"]/tr/th/div[2]/div[1]/a').click()

    def button3_click(self):
        """ 5. 点击三区中签到帖 """
        handles = self.driver.window_handles  # 切换窗口
        self.driver.switch_to.window(handles[-1])
        self.element.until(EC.presence_of_element_located((By.XPATH, '//*[@id="postmessage_26101770"]/strong[1]/a')))
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="postmessage_26101770"]/strong[1]/a').click()

    def switch_url(self):
        """ 6. 填写答卷信息 """
        try:
            time.sleep(5)
            self.driver.refresh()
            self.element.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/div/button[1]')))
            # time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/button[1]').click()
            time.sleep(3)
            self.driver.find_element_by_class_name("inputs-input").send_keys(self.qq_id)    # 输入QQ
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="question_q-2-evyZ"]/div[2]/div[1]/label/span').click()   # 一区
            # self.driver.find_element_by_xpath('//*[@id="question_q-2-evyZ"]/div[2]/div[2]/label').click()   # 二区
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="question_q-3-3fVQ"]/div[2]/div[1]/label/span').click()  # 签到类型
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="root-container"]/div/div[1]/div[1]/div[2]/div[3]/div/button').click()   # 提交
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="root-container"]/div/div[1]/div[1]/h3/div/p[3]/a').click()      # 跳转链接
        except Exception as e:
            print("登录失效，正在重新登录")
            self.login_qq2()

    def login_qq2(self):
        """ 6-1. 登录QQ """
        handles = self.driver.window_handles  # 切换窗口
        self.driver.switch_to.window(handles[-1])
        time.sleep(2)
        self.driver.switch_to.frame("ptlogin_iframe")   # 切换框架
        self.driver.find_element_by_id('switcher_plogin').click()  # 点击
        time.sleep(1)
        # 登录QQ
        self.driver.find_element_by_id('u').clear()
        self.driver.find_element_by_id('u').send_keys(self.qq_id)   # 输入
        self.driver.find_element_by_id('p').send_keys(self.qq_pas)
        time.sleep(1)
        self.driver.find_element_by_id('login_button').click()
        time.sleep(5)
        self.switch_url()

    def sign_in(self):
        handles = self.driver.window_handles    # 切换窗口
        self.driver.switch_to.window(handles[-1])
        time.sleep(5)
        self.driver.refresh()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="fastpostmessage"]').send_keys('{}已签到'.format(self.present_time))  # 签到
        self.driver.get_screenshot_as_file('签到成功截图.png')
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="fastpostsubmit"]').click()      # 提交
        time.sleep(3)
        self.driver.get_screenshot_as_file('打卡成功截图.png')
        time.sleep(2)
        self.driver.close()
        time.sleep(2)
        self.driver.quit()

    def run(self):
        """ 主要逻辑 """
        # 1. 打卡浏览器
        self.open_browser()
        time.sleep(3)
        # 2. 登录QQ
        self.login_qq()
        # 3. 点击体验服专区
        self.button1_click()
        # 4. 点击三区论坛
        self.button2_click()
        # 5. 点击签到贴
        self.button3_click()
        # 6. 填写答卷信息
        self.switch_url()
        print("正在签到")
        # 7. 签到
        self.sign_in()
        print("签到成功")


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    qq_id = '你的账号'
    qq_pas = '你的密码'
    dnf = DnfCheck(qq_id, qq_pas, option)
    dnf.run()
