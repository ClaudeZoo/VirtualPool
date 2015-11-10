# coding:utf-8
import subprocess


def shell(command):  # 执行脚本 返回脚本的返回值
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return s.communicate()