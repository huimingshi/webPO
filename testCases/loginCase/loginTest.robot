*** Settings ***
Library    ../../pageObj/LoginPage.py
Resource   ../../configs/all_user.robot

*** Test Cases ***
login_testcase_01
    ${driver1}   driver_set_up_and_logIn   ${call_oncall_user_username}    ${call_oncall_user_password}
    ${driver2}   driver_set_up_and_logIn   ${oncall_user_username}   ${oncall_user_password}