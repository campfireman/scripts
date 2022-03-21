#!/bin/bash

# based on: https://askubuntu.com/a/94861

# the system wide certificate registry
SYSTEM_CERT_DIR="/usr/share/ca-certificates/extra/"

# the folder containing the certificates to be added
# expects the certificates to be added to either end in .txt or .pem.txt
if [ -z $1 ]
  then echo "Please enter a folder containing the certificates"
  exit
fi
CERT_DIR=$1
echo ${HOME}
# make sure cert directory exists
sudo mkdir -p ${SYSTEM_CERT_DIR}

# Convert all certificates and add to all browsers
# thanks to https://web.archive.org/web/20210618230257/https://thomas-leister.de/en/how-to-import-ca-root-certificate/
for FILENAME in ${CERT_DIR}/*.txt; do
	FILE_DIR=$(dirname ${FILENAME})
	BASE_FILENAME=$(basename "${FILENAME}" .pem.txt)
	BASE_FILENAME=$(basename "${BASE_FILENAME}" .txt)
	CERT_FILEPATH="${FILE_DIR}/${BASE_FILENAME}.crt"

	# conversion
	echo "Converting ${FILENAME} to ${CERT_FILEPATH}"
	sudo openssl x509 -in "${FILENAME}" -inform PEM -out "${CERT_FILEPATH}"

	# search all cert DBs and add certificate to it
	for CERT_DB in $(find ${HOME} -name "cert9.db")
	do
		CERTDIR=$(dirname ${CERT_DB})
		echo "Adding ${BASE_FILENAME} ${CERT_DB} to certificate database in ${CERTDIR}"
		certutil -A -n "${BASE_FILENAME}" -t "TC,C,T" -i ${CERT_FILEPATH} -d sql:${CERTDIR}
	done
	# append empty line to create discernable block
	echo ""
done

echo "Copying all .crt certificates in ${CERT_DIR} to ${SYSTEM_CERT_DIR}"
sudo cp ${CERT_DIR}/*.crt ${SYSTEM_CERT_DIR}

echo "Adding certificates from ${SYSTEM_CERT_DIR} to /etc/ca-certificates.conf with update-ca-certificates"
sudo dpkg-reconfigure ca-certificates
