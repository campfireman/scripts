#! /usr/bin/python3

import json
import subprocess

with open('pkg_list.json', 'r') as file:
    pkg_list = json.loads(file.read())

    # install standard packages
    subprocess.call(['sudo', 'pacman', '--noconfirm',
                    '-S', *pkg_list['standard']])

    # install AUR packages
    subprocess.call(['yay', '--sudoloop',  '--answerclean',
                    'NotInstalled', '--answerdiff', 'None', '-S', *pkg_list['aur']])

    # install pip packages
    subprocess.call(['pip', 'install', *pkg_list['pip']])