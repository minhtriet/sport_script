# FORMAT: path num_frame class
# video_frame_path 100 10
# video_2_frame_path 150 31
# ...

from itertools import islice
import numpy as np
import sys
import pdb
import os
import json

sys.path.append('/media/data/mtriet/dataset/script/scnn/')
FRAME_PATH = "/media/data/mtriet/dataset/tsn_%s_frames" % sys.argv[1]
class_index = json.load() 

with open('/media/data/mtriet/dataset/script/%s/' % sys.argv[1], 'r') as f:
  class_index = json.load(f)
  events = [[]] * len(classes) 

CLASSES = [[]] * len(class_index)
if len(sys.argv) < 3:
  print('fb pad=True/False')
  sys.exit(1)
  
for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
  for folder in sub_folder:
    pdb.set_trace()
    klass = folder.split("_")[-1]
    sub_index = 0
    CLASSES[klass].append("%s/%s/ %d\n" % (frame_root, folder, CLASSES[klass]))

CLASSES = util.balance(CLASSES)
(x, y) = util.to_xy(CLASSES)
util.print_data_tsn('scnn_%s_train_proposal.lst' % sys.argv[1], 'scnn_%s_val_proposal.lst' % sys.argv[1], x, y)
