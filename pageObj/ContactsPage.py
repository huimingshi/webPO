# _*_ coding: utf-8 _*_ #
# @Time     :11/9/2022 11:07 AM
# @Author   :Huiming Shi

import time
from selenium.webdriver.common.keys import Keys
from commom.BasePage import BasePage
from configs.project_settings import IMPLICIT_WAIT
from pageEle.contactsPageEle import *
from pageEle.publicPageEle import *
from utils.handle_system_type import get_system_type
from selenium.webdriver import ActionChains


class ContactsPage(BasePage):
    def check_contacts_list(self,driver, *args):
        """
        获取并检查Contacts下Team页面的name列表
        :param driver:
        :param args: 预期的name列表
        :return:
        """
        # try:
        ele_list = self.get_xpath_elements(driver,
                                      '//div[@id="user-tabs-pane-team"]//div[@class="ag-center-cols-container"]/div//div[@class="cardName"]')
        print(ele_list)
        if len(args) != 0:
            for i in range(len(ele_list)):
                user_name = ele_list[i].get_attribute('textContent')
                self.public_assert(driver, args[i], user_name, condition='in', action='contacts列表name与预期不符')
        elif len(args) == 0:
            self.public_assert(driver, len(ele_list), 0, action='contacts列表name与预期不符')

    def open_send_meeting_dialog(self,driver, which_meeting):
        """
        # 打开发起MHS或者OTU会议的对话框
        :param driver:
        :param which_meeting: MHS或者OTU
        """
        self.public_click_element(driver, send_my_help_space_invitation, description='打开Send_My_Help_Space_Invitation窗口')
        if which_meeting == 'MHS':
            # 去勾选
            text_value = self.get_xpath_element(driver, checkbox_xpath, description='checkbox').get_attribute('value')
            if text_value == 'true':
                self.public_click_element(driver, checkbox_xpath, description='checkbox')
                time.sleep(2)
        elif which_meeting == 'OTU':
            # 勾选
            text_value = self.get_xpath_element(driver, checkbox_xpath, description='checkbox').get_attribute('value')
            if text_value == 'false':
                self.public_click_element(driver, checkbox_xpath, description='checkbox')
                time.sleep(2)

    def send_meeting_room_link(self,driver, which_meeting, if_send='no_send'):
        """
        # User发起MHS或者OTU会议，并且检查link的复制粘贴功能是否OK
        :param driver:
        :param which_meeting: MHS或者OTU
        :param if_send: 是否发送，‘send’表示发送，‘no_send’表示不发送，默认为no_send
        :return: MHS或者OTU会议的link
        """
        self.open_send_meeting_dialog(driver, which_meeting)
        # 复制
        for i in range(5):
            text = self.get_xpath_element(driver, '//div[@class="invite-link"]', description='邀请链接').get_attribute(
                "textContent")
            print(text)
            if text.startswith(r'https://'):
                break
            elif i == 4:
                self.public_check_element(driver,
                                     '//form[@class="InviteToHelpSpaceView form-horizontal"]//button[text()="Cancel"]',
                                     '点击取消按钮失败')
                self.open_send_meeting_dialog(driver, which_meeting)
                for i in range(5):
                    text = self.get_xpath_element(driver, '//div[@class="invite-link"]', description='邀请链接').get_attribute(
                        "textContent")
                    print(text)
                    if text.startswith(r'https://'):
                        break
                    elif i == 4:
                        self.screen_shot_func(driver, 'url信息未出现')
                        raise Exception
                    else:
                        time.sleep(10)
            else:
                time.sleep(10)
        self.public_check_element(driver, '//i[@class="far fa-copy "]', '复制按钮未出现')
        sys_type = get_system_type()
        if sys_type == 'Windows':
            ele = self.get_xpath_element(driver, my_help_space_message, description='message输入框')
            self.public_click_element(driver, my_help_space_message, description='message输入框')
            ele.send_keys(Keys.CONTROL, 'v')
        else:
            self.paste_on_a_non_windows_system(driver, my_help_space_message)
        # 验证复制后粘贴结果正确
        invite_url = self.get_xpath_element(driver, get_invite_link, description='邀请链接').get_attribute(
            "textContent")  # Get the invitation link
        print('复制的link为:', invite_url)
        attribute = self.get_xpath_element(driver, my_help_space_message, description='message输入框').get_attribute('value')
        print('粘贴的link为:', attribute)
        self.public_assert(driver, attribute, invite_url, action='复制和粘贴内容不一致')  # 验证复制后粘贴结果正确
        if if_send == 'send':
            # 输入email
            email_ele = self.get_xpath_element(driver, send_link_email_input, description='email输入框')
            self.public_click_element(driver, send_link_email_input, description='email输入框')
            email_ele.send_keys('Huiming.shi.helplightning+123456789@outlook.com')
            # 点击Send Invite按钮
            self.public_click_element(driver, send_link_send_invite, description='发送按钮')
        elif if_send == 'no_send':
            self.public_check_element(driver, '//div[@class="modal-content"]//button[text()="Cancel"]', '点击Cancel按钮失败')
        return invite_url

    def contacts_witch_page_make_call(self,driver1, driver2, witch_page, who='on-call group 1', accept='accept',
                                      audio='audio'):
        """
        Contacts页面进行call操作
        :param driver1:
        :param driver2:
        :param witch_page: 哪个page? Favorites/Team/Personal/Directory四个页面
        :param who: 与谁进行call? on-call group或者是某个user
        :param accept:对端是否accept此次call
        :return:
        """
        contacts_search_input_format = contacts_search_input.format(witch_page.lower())  # 目前只做了Contacts页面的make call
        # 查询on-call group或者是某个user
        element = self.get_xpath_element(driver1, contacts_search_input_format, description='查询框')
        element.clear()
        time.sleep(1)
        self.public_click_element(driver1, contacts_search_input_format, description='查询框')
        element.send_keys(who)
        time.sleep(5)
        contacts_search_result = f'//div[@id="user-tabs-pane-{witch_page.lower()}"]//div[text()="{who}"]'
        ele_ment = self.get_xpath_elements(driver1, contacts_search_result)
        print(f'{witch_page}输入框个数', len(ele_ment))
        if len(ele_ment) < 1:
            self.refresh_browser_page(driver1)
            element = self.get_xpath_element(driver1, contacts_search_input_format, description='搜索框')
            self.public_click_element(driver1, contacts_search_input_format, description='搜索框')
            element.send_keys(who)
            time.sleep(5)
        self.public_check_element(driver1, contacts_search_result, f'{who}未加载出', if_click=None, if_show=1)
        # 鼠标悬停
        ellipsis_xpath = f'//div[text()="{who}"]/../../../..//div[@class="ellipsis-menu-div"]'
        ellipsis = self.get_xpath_element(driver1, ellipsis_xpath, description='悬浮按钮')
        ActionChains(driver1).move_to_element(ellipsis).perform()
        # 选择Audio或者video
        if audio == 'audio':
            audio_xpath = f'//div[text()="{who}"]/../../../..//span[text()="Audio+"]/..'
            self.public_click_element(driver1, audio_xpath, description='启动Audio按钮')
        else:
            video_xpath = f'//div[text()="{who}"]/../../../..//span[text()="Video"]/..'
            self.public_click_element(driver1, video_xpath, description='启动Video按钮')
        # 需要Accept Declaimer
        driver1.implicitly_wait(5)
        count = self.get_xpath_elements(driver1, accept_disclaimer)
        if len(count) == 1:
            self.public_click_element(driver1, accept_disclaimer, '点击accept_disclaimer失败')
        driver1.implicitly_wait(IMPLICIT_WAIT)
        # 另一端ACCEPT OR DECLINE
        if accept == 'accept':
            self.public_check_element(driver2, anwser_call_button, '点击ANWSER按钮失败')
        elif accept == 'no_accept':
            self.public_check_element(driver2, decline_disclaimer, '点击DECLINE按钮失败')