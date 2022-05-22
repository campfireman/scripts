#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

setxkbmap -option caps:swapescape
$SCRIPT_DIR/cpfw.sh TCLAUSSE
