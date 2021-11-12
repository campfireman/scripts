#!/usr/bin/python3
"""In case tensorflow complains. C.f. https://archive.ph/LHQjZ"""

import subprocess

lspci_out = subprocess.check_output('lspci | grep VGA', shell=True)
pci_id = lspci_out.decode('utf-8').split(' ')[0]

print(f'Setting numa node of {pci_id} to 0')
subprocess.run(
    f'echo 0 | sudo tee -a /sys/bus/pci/devices/0000:{pci_id}/numa_node', shell=True)
