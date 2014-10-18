#!/usr/bin/env bash

function linstall.fonts.usage(){
    cat << EOF
Install some fonts (mostly chinese related) including: ttf-arphic-uming, ttf-wqy-microhei, ttf-wqy-zenhei, xfonts-wqy and fonts-sil-abyssinica.
Syntax: linstall.fonts
EOF
}

function linstall.fonts(){
    wajig install -y ttf-arphic-uming ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy fonts-sil-abyssinica
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.fonts $@
fi
