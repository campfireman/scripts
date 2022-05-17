import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description='Create WIFI QR codes with ease')
    parser.add_argument('ssid', type=str, help='The SSID of the network')
    parser.add_argument('pw', type=str, help='The password of the network')
    parser.add_argument('filename', type=str, help='The filename of the QR-code PNG (.png will be appended)')
    parser.add_argument('--size', type=int, default=9, help='The size of a dot or pixel (default = 9)')
    args = parser.parse_args()

    str_to_be_encoded = f'WIFI:T:WPA;S:{args.ssid};P:{args.pw};;'
    qualified_filename = f'{args.filename}.png'
    subprocess.run(['qrencode', str_to_be_encoded, '-o', qualified_filename, '-s', str(args.size)])


if __name__ == '__main__':
    main()