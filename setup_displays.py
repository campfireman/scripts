#!/usr/bin/env python3

import json
import os
import subprocess
from argparse import ArgumentParser


def main():
    script_dir = os.path.dirname(__file__)

    parser = ArgumentParser()
    parser.add_argument(
        'device_name',
        type=str,
        help='The device name in the settings file',
    )
    parser.add_argument(
        'setup_name',
        type=str,
        help='The name of the setup for a given device',
    )
    args = parser.parse_args()

    with open(os.path.join(script_dir, "assets", "display_settings.json")) as settings_file:
        settings = json.loads(settings_file.read())

    try:
        setup = settings[args.device_name][args.setup_name]
    except KeyError:
        raise Exception(
            f'Setup not found for device {args.device_name} and setup {args.setup_name}!')

    for display, display_command in setup.items():
        command = f'xrandr --output {display} {display_command}'
        print(f'Running command: {command}')
        exit_code = subprocess.call(command.split(' '))
        if exit_code != 0:
            raise Exception(f'Command {command} return non 0 exit code!')


if __name__ == '__main__':
    main()
