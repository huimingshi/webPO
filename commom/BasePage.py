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
from utils.handle_path import current_project_path
import sys

class BasePage(object):
    def get_system_type(self):
        """
        # get current system type
        # Windows or Mac
        :return: system type
        """
        system_type = platform.system()
        print(system_type)
        return system_type

    def kill_all_browser(self):
        system_type = self.get_system_type()
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
        sys_type = self.get_system_type()
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

    def get_picture_path(self,picture_name='avatar1.jpg'):
        """
        # 获取avatar1.jpg绝对路径
        :return: avatar1.jpg绝对路径
        """
        dir_path = os.path.dirname(os.path.abspath(__file__))
        print('当前目录绝对路径:', dir_path)
        system_type = self.get_system_type()
        if system_type == 'Windows':
            dir_list = dir_path.split('\\')
            print(dir_list)
            dir_list[-1] = 'publicData'
            join_str = '\\\\'
            final_path = join_str.join(dir_list)
            modify_picture_path = final_path + f'\\\\{picture_name}'
            return modify_picture_path
        else:
            dir_list = dir_path.split('/')
            print(dir_list)
            dir_list[-1] = 'publicData'
            join_str = '//'
            final_path = join_str.join(dir_list)
            print(final_path)
            modify_picture_path = final_path + f'//{picture_name}'
            print(modify_picture_path)
            return modify_picture_path

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


def add_to_pythonpath():
    sys.path.insert(0, current_project_path)