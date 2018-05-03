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
from subtitle import Subtitle
import util

FRAME_PATH = "/media/data/mtriet/dataset/tsn_%s_frames" % sys.argv[1]
SUB_PATH = "/media/data/mtriet/raw_video/%s/train" % (sys.argv[1])
OVERLAP_RATE = 0.75
CLASSES = [[], []]  # 0, 1

if len(sys.argv) < 3:
  print('fb pad=True/False')
  sys.exit(1)
  
for window_size in WINDOW_SIZE:
  for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
    for folder in sub_folder:       
      subtitles = Subtitle.load_subtitle(SUB_PATH, folder, sys.argv[2]) 
      frames = sorted(os.listdir(frame_root + '/' + folder))
      sub_index = 0
      for begin_pivot in range(1, len(frames) - window_size, int(window_size*(1 - OVERLAP_RATE))):  # ignore last few frames
        if (begin_pivot > subtitles[sub_index].end) and (sub_index < len(subtitles) - 1):
          sub_index += 1 

        end_pivot = min(begin_pivot + window_size, len(frames))
        segment = range(begin_pivot, begin_pivot + window_size + 1)
        sub_range = subtitles[sub_index].get_range()
        intersection = np.intersect1d(segment, sub_range)
        if len(intersection) == len(segment):        # the subtitle contains the segment
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
