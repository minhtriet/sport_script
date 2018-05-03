# proposal needs to see the all augemented data
# build based on folder structure

from itertools import islice
import numpy as np
import sys
import pdb
import os
import json

sys.path.append('../scnn/')

FRAME_PATH = "/media/data/mtriet/dataset/tsn_%s_frames" % sys.argv[1]
CLASSES = json.load('/media/data/mtriet/dataset/script/%s/' % sys.argv[1]) 

if len(sys.argv) < 3:
  print('fb pad=True/False')
  sys.exit(1)
  
for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
  for folder in sub_folder:
    frames = sorted(os.listdir(frame_root + '/' + folder))
    sub_index = 0
    CLASSES[1].append("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 1, window_size/16))    
  elif len(intersection) == 0:        # not contains at all 
    CLASSES[0].append("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 0, window_size/16))    
  else:
    union = len(segment) + len(sub_range) - len(intersection)
    current_score = 1.0 * len(intersection) / union 
    if current_score > 0.7:
      CLASSES[1].append("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 1, window_size/16))    
    else:  # check if next segment has better score, if > 0.7, and if max of them > 0.5
      if sub_index == len(subtitles) - 1: # already at last subtitle
        CLASSES[0].append("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 0, window_size/16))    
      else:
        sub_range = subtitles[sub_index+1].get_range()
        intersection = np.intersect1d(segment, sub_range)
        next_score = 1.0 * len(intersection) / union 
        if max(current_score, next_score) > 0.5:
          CLASSES[1].append("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 1, window_size/16))    
        else:
          CLASSES[0].append("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 0, window_size/16))

CLASSES = util.balance(CLASSES)
(x, y) = util.to_xy(CLASSES)
util.print_data('scnn_%s_train_proposal.lst' % sys.argv[1], 'scnn_%s_val_proposal.lst' % sys.argv[1], x, y)
