#! /usr/bin/python3

import json
import os
import subprocess

with open(os.path.join(os.path.dirname(__file__), 'assets', 'pkg_list.json'), 'r') as file:
    pkg_list = json.loads(file.read())

    # install standard packages
    subprocess.call(['sudo', 'pacman', '--noconfirm',
                    '-S', *pkg_list['standard']])

    # install AUR packages
    subprocess.call(['yay', '--sudoloop',  '--answerclean',
                    'NotInstalled', '--answerdiff', 'None', '-S', *pkg_list['aur']])

    # install pip packages
    subprocess.call(['pip', 'install', *pkg_list['pip']])

    # install cpan packages
    subprocess.call(['sudo', 'cpan', *pkg_list['cpan']])
