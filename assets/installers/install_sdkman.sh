#! /bin/bash

curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk version

sdk install java 17.0.2-open
sdk install java 11.0.12-open
sdk install java 8.0.302-open

sdk install maven 3.8.5
