#!/bin/bash

SCRIPT_PATH=$(dirname ${0})
ansible-playbook -i ${SCRIPT_PATH}/inventory ${SCRIPT_PATH}/manjaro_sway.yml

