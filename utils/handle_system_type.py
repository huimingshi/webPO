# _*_ coding: utf-8 _*_ #
# @Time     :11/9/2022 11:21 AM
# @Author   :Huiming Shi

import platform

def get_system_type():
    """
    # get current system type
    # Windows or Mac
    :return: system type
    """
    system_type = platform.system()
    print(system_type)
    return system_type