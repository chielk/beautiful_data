#!/bin/bash
wget https://www.dropbox.com/s/4rdxz4uf2kcrs4y/MysteryData.zip?dl=0 -O \
	MysteryData.zip
unzip MysteryData.zip
mkdir -p data
mv slice* data
rm MysteryData.zip
