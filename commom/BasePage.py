# _*_ coding: utf-8 _*_ #
# @Time     :11/8/2022 3:37 PM
# @Author   :Huiming Shi

import os
import platform
import time
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from configs.project_settings import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pageEle.publicPageEle import close_tutorial_button
from utils.handle_system_type import get_system_type


class BasePage(object):
    def kill_all_browser(self):
        system_type = get_system_type()
        if system_type == 'Windows':
            if SMALL_RANGE_BROWSER_TYPE == 'Chrome':
                # kill所有的chromedriver进程
                os.system('taskkill /F /im chromedriver.exe')
                # 退出所有的浏览器，也会kill所有的chromedriver进程
                os.system('taskkill /f /t /im chrome.exe')
            if CITRON_BROWSER_TYPE == 'Chrome':
                # kill所有的chromedriver进程
                os.system('taskkill /F /im chromedriver.exe')
                # 退出所有的浏览器，也会kill所有的chromedriver进程
                os.system('taskkill /f /t /im chrome.exe')
            if SMALL_RANGE_BROWSER_TYPE == 'Firefox':
                # kill所有的firefoxdriver进程
                os.system("taskkill /im geckodriver.exe /f")
                # 退出所有的浏览器，也会kill所有的firefoxdriver进程
                os.system('taskkill /f /t /im firefox.exe')
            if CITRON_BROWSER_TYPE == 'Firefox':
                # kill所有的firefoxdriver进程
                os.system("taskkill /im geckodriver.exe /f")
                # 退出所有的浏览器，也会kill所有的firefoxdriver进程
                os.system('taskkill /f /t /im firefox.exe')
        else:
            if SMALL_RANGE_BROWSER_TYPE == 'Chrome':
                # kill所有的chromedriver进程
                os.system("kill -9 `ps -ef | grep chromedriver  | awk '{print $2}'`")
                # 退出所有的浏览器，也会kill所有的chromedriver进程
                os.system("kill -9 `ps -ef | grep hrome  | awk '{print $2}'`")
            if CITRON_BROWSER_TYPE == 'Chrome':
                # kill所有的chromedriver进程
                os.system("kill -9 `ps -ef | grep chromedriver  | awk '{print $2}'`")
                # 退出所有的浏览器，也会kill所有的chromedriver进程
                os.system("kill -9 `ps -ef | grep hrome  | awk '{print $2}'`")
            if SMALL_RANGE_BROWSER_TYPE == 'Firefox':
                # kill所有的firefoxdriver进程
                os.system("kill -9 `ps -ef | grep geckodriver  | awk '{print $2}'`")
                # 退出所有的浏览器，也会kill所有的firefoxdriver进程
                os.system("kill -9 `ps -ef | grep irefox  | awk '{print $2}'`")
            if CITRON_BROWSER_TYPE == 'Firefox':
                # kill所有的firefoxdriver进程
                os.system("kill -9 `ps -ef | grep geckodriver  | awk '{print $2}'`")
                # 退出所有的浏览器，也会kill所有的firefoxdriver进程
                os.system("kill -9 `ps -ef | grep irefox  | awk '{print $2}'`")

    def screen_shot_func(self,driver, screen_name):
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        sys_type = get_system_type()
        if sys_type == 'Windows':
            driver.save_screenshot('.\\' + current_time + screen_name + 'screenshot.png')
        else:
            driver.save_screenshot('./' + current_time + screen_name + 'screenshot.png')

    def get_xpath_element(self,driver, locator, ec=None, select='xpath', description='元素', timeout=WEBDRIVERWAIT_TIMEOUT):
        """
        通过xpath寻找元素，driver.find_element_by_xpath(xpath)
        :param driver: 浏览器驱动
        :param locator: 元素的locator
        :param ec: 是否需要使用EC来进行显示等待，默认需要
        :param select: 默认是xpath寻找，也可以进行切换成id
        :param description: 描述信息
        :return:
        """
        if not ec:
            try:
                return WebDriverWait(driver, timeout, POLL_FREQUENCY).until(
                    EC.visibility_of_element_located((select, locator)))
            except Exception as e:
                print('元素未找到', e)
                msg = traceback.format_exc()
                print(msg)
                self.screen_shot_func(driver, f'{description}未找到')
                raise Exception
        else:
            return driver.find_element(select, locator)

    def get_xpath_elements(self,driver, xpath):
        """
        通过xpath寻找元素，driver.find_element_by_xpath(xpath)
        :param driver: 浏览器驱动
        :param xpath: 元素的xpath
        :return:
        """
        elements_list = driver.find_elements('xpath', xpath)
        return elements_list

    def public_click_element(self,driver, locator, ec=None, select='xpath', description='元素'):
        """
        通过xpath点击元素
        :param driver: 浏览器驱动
        :param locator: 元素的locator
        :param ec: 是否需要使用EC来进行显示等待，默认需要
        :param select: 默认是xpath寻找，也可以进行切换成id
        :return:
        """
        try:
            self.get_xpath_element(driver, locator, ec, select, description).click()
        except Exception as e:
            print('元素不可点击', e)
            msg = traceback.format_exc()
            print(msg)
            self.screen_shot_func(driver, f'{description}不可点击')
            raise Exception

    def public_check_element(self,driver, xpath, description, if_click=1, if_show=1):
        """
        :param driver:
        :param xpath:   元素的xpath
        :param if_show:   是否需要出现该元素
        :param if_click:    是否需要点击
        :param description:    元素未出现的描述信息
        :return:
        """
        for i in range(5):
            time.sleep(2)
            ele_list = self.get_xpath_elements(driver, xpath)
            if if_show and if_click:
                if len(ele_list) >= 1:
                    self.public_click_element(driver, xpath, description=description)
                    break
            elif if_show and not if_click:
                if len(ele_list) >= 1:
                    break
            elif not if_show:
                if len(ele_list) == 0:
                    break
            elif i == 4:
                print(description)
                self.screen_shot_func(driver, description)
                raise Exception

    def public_assert(self,driver, string1, string2, condition='=', action=None):
        """
        公共的断言方法
        :param driver:
        :param string1:
        :param string2:
        :param condition:
        :param action:
        :return:
        """
        try:
            if condition == '=':
                assert string1 == string2
            elif condition == 'in':
                assert string1 in string2
            elif condition == 'not in':
                assert string1 not in string2
            elif condition == '!=':
                assert string1 != string2
            elif condition == '>=':
                assert string1 >= string2
            elif condition == 'startswith':
                assert string1.startswith(string2)
        except AssertionError:
            self.screen_shot_func(driver, action)
            raise AssertionError

    def paste_on_a_non_windows_system(self,driver, paste_xpath):
        """
        非windows系统上粘贴
        :param driver:
        :param paste_xpath:需要进行粘贴的元素的xpath
        :return:
        """
        ele = self.get_xpath_element(driver, paste_xpath, description='非Windows操作系统粘贴')
        actions = ActionChains(driver)
        actions.move_to_element(ele)
        actions.click(ele)  # select the element where to paste text
        actions.key_down(Keys.META)
        actions.send_keys('v')
        actions.key_up(Keys.META)
        actions.perform()

    def refresh_browser_page(self,driver, close_tutorial='close_tutorial'):
        """
        刷新浏览器的某个页面
        :param driver:
        :param close_tutorial: 是否关闭导航页面；默认关闭
        :return:
        """
        driver.refresh()
        if close_tutorial == 'close_tutorial':
            self.close_tutorial_action(driver)

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