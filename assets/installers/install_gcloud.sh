
VERSION=385.0.0
# INSTALL_FOLDER=/opt/gcloud
INSTALL_FOLDER=${HOME}/google-cloud-sdk
COMPONENTS=(alpha beta)

sudo mkdir -p ${INSTALL_FOLDER}
sudo chown ${USER} ${INSTALL_FOLDER}


cd /tmp
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${VERSION}-linux-x86_64.tar.gz

tar -xf google-cloud-cli-${VERSION}-linux-x86_64.tar.gz

mv google-cloud-sdk/* ${INSTALL_FOLDER}

${INSTALL_FOLDER}/install.sh --quiet

${INSTALL_FOLDER}/bin/gcloud init

source ${INSTALL_FOLDER}/completion.bash.inc
source ${INSTALL_FOLDER}/path.bash.inc

# cat << EOF >> ${HOME}/.profile

# # gcloud installation
# source ${INSTALL_FOLDER}/completion.zsh.inc
# source ${INSTALL_FOLDER}/path.zsh.inc
# EOF

gcloud components update
gcloud config set disable_usage_reporting false

for component_id in COMPONENTS; do
	gcloud components install component_id
done
