# FORMAT: path num_frame class
# video_frame_path 100 10
# video_2_frame_path 150 31
# ...

import sys
import pdb
import os
import json

sys.path.append('/media/data/mtriet/dataset/script/scnn/')

import util

FRAME_PATH = "/media/data/mtriet/dataset/tsn_%s_frames" % sys.argv[1]

with open('/media/data/mtriet/dataset/script/%s_origin_classes_wo_bg.json' % sys.argv[1], 'r') as f:
  class_index = json.load(f)

CLASSES = [[] for _ in range(len(class_index))]
if len(sys.argv) < 2:
  print('fb/bb')
  sys.exit(1)
print(class_index)
for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
  for folder in sub_folder:
    klass = folder.split("_")[-1]
    klass = class_index[klass]
    frane_cnt = len(os.listdir('%s/%s' % (frame_root, folder))) / 3
    CLASSES[klass].append("%s/%s/ %d %d\n" % (frame_root, folder, frane_cnt, klass))

CLASSES = util.balance(CLASSES) 
(x, y) = util.to_xy(CLASSES)
util.print_data('tsn_%s_train.lst' % sys.argv[1], 'tsn_%s_val.lst' % sys.argv[1], x, y)
