#!/bin/bash

cd /tmp

folder_name=intellij-ultimate

echo "Downloading files"
link="https://download.jetbrains.com/product?code=IIU&latest&distribution=linux"
wget $link -O output.tar.gz
#sudo curl -L $link | sudo tar xvz -C $folder_name --strip 1

echo "Creating symlink"
sudo ln -s /opt/intellij-ultimate/bin/idea.sh /usr/bin/intellij-ultimate
