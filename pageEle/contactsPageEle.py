# _*_ coding: utf-8 _*_ #
# @Time     :11/9/2022 11:10 AM
# @Author   :Huiming Shi

send_my_help_space_invitation = '//button[contains(.,"Send My Help Space Invitation")]'
checkbox_xpath = '//input[@name="oneTime" and @type="checkbox"]'
my_help_space_message = '//input[@name="message"]'
get_invite_link = '//div[@class="invite-link"]'
send_link_email_input = '//input[@placeholder="Participant email"]'    # 发送link时的email输入框xpath
send_link_send_invite = '//button[contains(.,"Send Invite")]'          # 发送link时的Send Invite按钮
contacts_search_input = '//div[@id="user-tabs-pane-{}"]//input[@id="filter-text-box"]'