#!/bin/bash

### Copyright @ Cornelius Buschka ###

LOCAL_BIN=${HOME}/.local/bin

mkdir -p ${LOCAL_BIN}
if [ ! -f "${LOCAL_BIN}/cpfw-login" ]; then
	  curl -L -o /tmp/cpfw-login_amd64 https://github.com/felixb/cpfw-login/releases/download/v0.3/cpfw-login_amd64 
	  mv /tmp/cpfw-login_amd64 ${LOCAL_BIN}/cpfw-login
	  chmod 755 ${LOCAL_BIN}/cpfw-login
fi
if [ "0" = "$#" ]; then
	  echo
	  echo " cpfw-loginw <username>"
	  echo
	  exit 1
fi
CHECKSUM=$(md5sum ${LOCAL_BIN}/cpfw-login | cut -c 1-32)
echo "${CHECKSUM}"
if [ "${CHECKSUM}" != "c2dde67520efc0d192a60dba1d228658" ]; then
	  echo "cpfw-login is broken."
	  exit 1
fi
exec ${LOCAL_BIN}/cpfw-login --url https://fwauth.ov.otto.de --user ${1} --passwordprompt

