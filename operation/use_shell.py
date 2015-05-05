__author__ = 'Claude'

import subprocess


def shell(command):
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return s.communicate()