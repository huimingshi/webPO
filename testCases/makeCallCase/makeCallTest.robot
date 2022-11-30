*** Settings ***
Library    ../../pageObj/LoginPage.py
Library    ../../pageObj/ContactsPage.py
Resource   ../../configs/all_user.robot
Resource   ../../configs/PublicParams.robot

*** Test Cases ***
login_testcase_01
    [Documentation]    两个用户进行通话
    [Tags]    call_test_case
    ${driver1}   driver_set_up_and_logIn    ${message_test0_user}
    ${driver2}   driver_set_up_and_logIn    ${message_test1_user}
    contacts_witch_page_make_call     ${driver1}    ${driver2}   ${py_team_page}   ${message_test1_username}