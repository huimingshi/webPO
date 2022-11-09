# _*_ coding: utf-8 _*_ #
# @Time     :11/8/2022 4:30 PM
# @Author   :Huiming Shi
import os,sys

# 当前项目的绝对路径
current_project_path = os.path.dirname(os.path.abspath(os.curdir))
# print(current_project_path)

def get_picture_path(picture_name='avatar1.jpg'):
    """
    # 获取avatar1.jpg绝对路径
    :return: avatar1.jpg绝对路径
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    print('当前目录绝对路径:', dir_path)
    system_type = get_system_type()
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

if __name__ == '__main__':
    import sys
    sys.path.insert(0, current_project_path)
    print(sys.path)