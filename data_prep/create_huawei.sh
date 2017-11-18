#!/usr/bin/env sh

TOOLS=/media/data/mtriet/cdc/CDC/build/tools/
DATA=/media/data/mtriet/dataset/

echo "Creating leveldb..."

rm -rf "$1"_leveldb

if [[ $1 != 'fb' ]] && [[ $1 != 'bb' ]]; then
    echo 'finetune <fb/bb>'
    exit
else
    GLOG_logtostderr=1 $TOOLS/convert_imageset.bin \
    / \
    $DATA/"$1"_frames_list.txt \
    "$1"_leveldb 1 
    echo "Done."
fi
