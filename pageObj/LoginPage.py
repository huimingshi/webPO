# _*_ coding: utf-8 _*_ #
# @Time     :11/8/2022 3:47 PM
# @Author   :Huiming Shi

from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from commom.BasePage import BasePage
from configs.project_settings import *
import time
from pageEle.loginPageEle import *
from pageEle.publicPageEle import *


# 定义一个装饰器，当打开citron时出现WebDriverException：ERR_NAME_NOT_RESOLVED时进行截图



def ERR_NAME_NOT_RESOLVED(func):
    def inner(self,driver, *args, **kwargs):
        try:
            func(self,driver, *args, **kwargs)
        except WebDriverException:
            print('网页打开报错')
            self.screen_shot_func(driver,'网页打开报错')
            raise WebDriverException('网页打开报错')
    return inner

if SMALL_RANGE_BROWSER_TYPE == 'Chrome':
        from selenium.webdriver.chrome.options import Options
        optionc = Options()
        optionc.add_argument("--disable-infobars")
        optionc.add_argument("start-maximized")
        optionc.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        optionc.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1,  # chrome开启通知
            "profile.default_content_setting_values.media_stream_mic": 1,  # chrome开启麦克风
            "profile.default_content_setting_values.media_stream_camera": 1  # chrome开启摄像头
        })
        # 忽略证书错误，不需要手动点高级选项
        optionc.add_argument('--ignore-certificate-errors')

elif SMALL_RANGE_BROWSER_TYPE == 'Firefox':
    from selenium.webdriver.firefox.options import Options
    optionf = Options()
    optionf.add_argument("--disable-infobars")
    optionf.add_argument("start-maximized")
    optionf.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    optionf.set_capability("prefs", {
        "profile.default_content_setting_values.notifications": 1,
        "profile.default_content_setting_values.media_stream_mic": 1
    })
    # 忽略证书错误，不需要手动点高级选项
    optionf.add_argument('--ignore-certificate-errors')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en-US, en')
    profile.set_preference("permissions.default.microphone", 1)
    profile.set_preference("webdriver_accept_untrusted_certs", True)
    profile.set_preference("browser.link.open_newwindow", 3)
    profile.set_preference("browser.link.open_newwindow.restriction", 2)
    profile.set_preference("browser.tabs.remote.autostart", False)
    profile.set_preference("browser.tabs.remote.autostart.1", False)
    profile.set_preference("browser.tabs.remote.autostart.2", False)

class LoginPage(BasePage):
    def start_an_empty_window(self):
        """
        启动一个空的窗口
        :return:
        """
        if SMALL_RANGE_BROWSER_TYPE == 'Chrome':
            driver = webdriver.Chrome(options=optionc)
        elif SMALL_RANGE_BROWSER_TYPE == 'Firefox':
            driver = webdriver.Firefox(options=optionf, firefox_profile=profile)
        driver.implicitly_wait(int(IMPLICIT_WAIT))
        driver.maximize_window()
        return driver

    @ERR_NAME_NOT_RESOLVED
    def open_citron_url(self,driver):
        """
        打开Citron网址
        :param driver:
        :return:
        """
        driver.get(TEST_WEB)

    @ERR_NAME_NOT_RESOLVED
    def logIn_citron(self,driver, username, password, check_toturial='no_check_toturial', close_bounced='close_bounced',
                     accept='accept', disturb='not_set_disturb'):
        """
        封装页面的登录操作和关闭弹框操作
        :param driver: 浏览器驱动
        :param username: 用户名
        :param password: 密码
        :param close_bounced: 是否关闭教程，默认关闭
        :param accept: 是否接受免责声明，默认accept接受
        :param disturb: 是否设置为免打扰模式，默认not_set_disturb不设置；set_disturb为设置
        :param check_toturial:是否检查导航页面的welcome信息，默认不检查no_check_toturial，检查check_toturial
        :return:
        """
        # try:    # enter email
        self.public_click_element(driver, username_input, description='用户名输入框')
        self.get_xpath_element(driver, username_input, description='用户名输入框').send_keys(username)
        username_value = self.get_xpath_element(driver, username_input, description='用户名输入框').get_attribute('value')
        if username_value == username:
            time.sleep(1)
            self.public_click_element(driver, next_button, description='NEXT按钮')
        # 输入密码
        driver.implicitly_wait(0.1)
        # try:
        for i in range(100):
            time.sleep(1)
            ele_list = self.get_xpath_elements(driver, '//input[@style="display: block;"]')
            ele_list_next = self.get_xpath_elements(driver, next_button)
            if len(ele_list) == 1:
                self.get_xpath_element(driver, password_input, description='密码输入框').send_keys(password)
                self.public_click_element(driver, login_button, description='LOGIN按钮')
                time.sleep(1)
                break
            elif len(ele_list_next) == 1:
                self.public_click_element(driver, next_button, description='NEXT按钮')
            elif i == 99:
                print('password输入框还是未出现')
                self.screen_shot_func(driver, '登陆时输入password失败')
                raise Exception('password输入框还是未出现')
        # 校验是否进入到主页
        for i in range(200):
            time.sleep(1)
            currentPageUrl = driver.current_url
            print("当前页面的url是：", currentPageUrl)
            if currentPageUrl == TEST_WEB:
                break
            ele_list_login = self.get_xpath_elements(driver, login_button)
            if len(ele_list_login) == 1:
                self.public_click_element(driver, login_button, description='LOGIN按钮')
            elif i == 199:
                print('再次点击登录按钮未进入首页')
                self.screen_shot_func(driver, '再次登陆失败')
                raise Exception('再次点击登录按钮未进入首页')
        # close Disclaimer
        driver.implicitly_wait(int(6))
        if accept == 'accept':
            count = self.get_xpath_elements(driver, accept_disclaimer)
            if len(count) == 1:  # close Disclaimer
                self.public_click_element(driver, accept_disclaimer, description='接受Disclaimer按钮')
        # close Tutorial
        if close_bounced == 'close_bounced':
            # check Tutorial
            if check_toturial == 'check_toturial':
                ele_list = self.get_xpath_elements(driver, '//h1[text()="Welcome to Help Lightning!"]')
                self.public_assert(driver, len(ele_list), 1, condition='=', action='展示的不是Welcome to Help Lightning!')
            # close Tutorial
            self.close_tutorial_action(driver)
            # ele_list = get_xpath_elements(driver,close_tutorial_button)
            # if len(ele_list) == 1:
            #     public_click_element(driver, close_tutorial_button, description='关闭tutorial按钮')
        if disturb == 'not_set_disturb':
            ele_list = self.get_xpath_elements(driver, not_disturb)
            if len(ele_list) == 0:
                self.public_click_element(driver, make_available_button, description='make_available按钮')
        elif disturb == 'set_disturb':
            self.set_do_not_disturb(driver)
        driver.implicitly_wait(int(IMPLICIT_WAIT))

    def driver_set_up_and_logIn(self,username, password='*IK<8ik,8ik,', check_toturial='no_check_toturial',
                                close_bounced='close_bounced', accept='accept', disturb='not_set_disturb'):
        """
        # driver set up And LogIn
        :param username: 用户名
        :param password: 密码
        :param close_bounced: 是否关闭教程，默认关闭
        :param accept: 是否接受免责声明，默认accept接受
        :param disturb: 是否设置为免打扰模式，默认not_set_disturb不设置；set_disturb为设置
        :param check_toturial:是否检查导航页面的welcome信息，默认不检查no_check_toturial，检查check_toturial
        :return:
        """
        driver = self.start_an_empty_window()
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self.open_citron_url(driver)
        self.logIn_citron(driver, username, password, check_toturial, close_bounced, accept, disturb)
        return driver

    def set_do_not_disturb(self,driver):
        """
        User设置比Do Not Disturb请勿打扰模式
        :param driver:
        :return:
        """
        # try:
        ele_list = self.get_xpath_elements(driver, not_disturb)
        if len(ele_list) == 1:
            self.public_click_element(driver, not_disturb, description='not_disturb按钮')
            textarea_ele = self.get_xpath_element(driver, '//textarea[@placeholder="Status Message (optional)"]',
                                             description='请勿打扰输入框')
            self.public_click_element(driver, '//textarea[@placeholder="Status Message (optional)"]', description='请勿打扰输入框')
            textarea_ele.send_keys('Please Do not disturb')
            self.public_click_element(driver, '//button[@type="submit" and text()="Save"]', description='保存按钮')
            ele_list = self.get_xpath_elements(driver, make_available_button)
            self.public_assert(driver, len(ele_list), 1, condition='=', action='设置免打扰模式失败')
            assert len(ele_list) == 1
        textContent = self.get_xpath_element(driver, '//div[@role="alert"]/div', description='免受打扰文本').get_attribute(
            'textContent')
        print(textContent)
        self.public_assert(driver, textContent, 'Your status is currently set to Do Not Disturb.Make Available',
                      condition='=', action='设置免打扰模式后文本信息不正确')

    def close_tutorial_action(self,driver):
        """
        关闭导航页面
        :param driver:
        :return:
        """
        for i in range(3):
            ele_list = self.get_xpath_elements(driver, close_tutorial_button)
            if len(ele_list) == 1:
                self.public_click_element(driver, close_tutorial_button, description='close_tutorial按钮')
                break
            elif i == 2:
                self.public_assert(driver, len(ele_list), 1, action='关闭导航页面未出现')
            else:
                time.sleep(10)