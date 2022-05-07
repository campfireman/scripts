#!/usr/bin/env python3

import subprocess
from typing import List


def run_and_print(cmd: List[str]) -> None:
    output = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(output.stdout.decode('utf-8'))


def main():
    run_and_print(['xinput', 'list'])
    device_number = input('Enter a device number: ')
    run_and_print(['xinput', 'list-props', device_number])
    while True:
        property_number = input('Enter a property number: ')
        property_value = input('Enter a property value: ')
        run_and_print(['xinput', 'set-prop', device_number,
                       property_number,  property_value])
        shall_continue = input(
            'Set another property for this device? [y/N]?: ').lower()
        if shall_continue == 'y' or shall_continue == 'yes':
            continue
        break


if __name__ == '__main__':
    main()
