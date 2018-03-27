# proposal needs to see the all augemented data

from itertools import islice
import numpy as np
import sys
import pdb
import os
import json
from subtitle import Subtitle
import random

FRAME_PATH = "/media/data/mtriet/dataset/scnn_%s_frames" % sys.argv[1]
SUB_PATH = "/media/data/mtriet/raw_video/%s/%s" % (sys.argv[1], sys.argv[2])
WINDOW_SIZE = [16,32,64,128,256,512] 
OVERLAP_RATE = 0.75
ZERO_OUPUT_PROBABILITY = 0.2
TRAIN_VAL_SPLIT = 0.8

def print_data(train_file, val_file, frame_root, folder, begin_pivot, klass, window_size):
  if klass == 1:
    if random.random() < TRAIN_VAL_SPLIT:
      train_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))    
      train_file.write("%s/%s/ %06d %d %d\n" % (frame_root + '_augment', folder, begin_pivot, klass, window_size/16))
    else:
      val_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))
      val_file.write("%s/%s/ %06d %d %d\n" % (frame_root + '_augment', folder, begin_pivot, klass, window_size/16))
  else:
    if random.random() < ZERO_OUPUT_PROBABILITY: 
      if random.random() < TRAIN_VAL_SPLIT: 
        train_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))
        train_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))    
      else:
        val_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))
        val_file.write("%s/%s/ %06d %d %d\n" % (frame_root + '_augment', folder, begin_pivot, klass, window_size/16))


if len(sys.argv) < 4:
  print('fb train/val pad=True/False')
  sys.exit(1)
  
with open('scnn_%s_train_proposal.lst' % sys.argv[1], 'w') as train_file:
  with open('scnn_%s_val_proposal.lst' % sys.argv[1], 'w') as val_file:
    for window_size in WINDOW_SIZE:
      for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
        for folder in sub_folder:       
          print folder
          subtitles = Subtitle.load_subtitle(folder, sys.argv[3]) 
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
                  print_data(train_file, val_file, frame_root, folder, begin_pivot, 1, window_size)
              elif len(intersection) == 0:        # not contains at all 
                  print_data(train_file, val_file, frame_root, folder, begin_pivot, 0, window_size)
              else:
                  union = len(segment) + len(sub_range) - len(intersection)
                  current_score = 1.0 * len(intersection) / union 
                  if current_score > 0.7:
                      print_data(train_file, val_file, frame_root, folder, begin_pivot, 1, window_size)
                  else:  # check if next segment has better score, if > 0.7, and if max of them > 0.5
                      if sub_index == len(subtitles) - 1: # already at last subtitle
                          print_data(train_file, val_file, frame_root, folder, begin_pivot, 0, window_size)
                      else:
                          sub_range = subtitles[sub_index+1].get_range()
                          intersection = np.intersect1d(segment, sub_range)
                          next_score = 1.0 * len(intersection) / union 
                          if max(current_score, next_score) > 0.5:
                              print_data(train_file, val_file, frame_root, folder, begin_pivot, 1, window_size)
                          else:
                              print_data(train_file, val_file, frame_root, folder, begin_pivot, 0, window_size)
