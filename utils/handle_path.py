# _*_ coding: utf-8 _*_ #
# @Time     :11/8/2022 4:30 PM
# @Author   :Huiming Shi
import os,sys

# 当前项目的绝对路径
current_project_path = os.path.dirname(os.path.abspath(os.curdir))
# print(current_project_path)


if __name__ == '__main__':
    import sys
    sys.path.insert(0, current_project_path)
    print(sys.path)