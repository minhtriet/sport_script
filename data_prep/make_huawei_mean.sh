#!/usr/bin/env sh
TOOLS=/media/data/mtriet/cdc/CDC/build/tools

if [[ $1 != 'fb' ]] && [[ $1 != 'bb' ]]; then
    echo 'make_huawei_mean <fb/bb>'
    exit
else
  $TOOLS/compute_image_mean.bin "$1"_leveldb "$1"_mean.binaryproto
  echo "Done."
fi
