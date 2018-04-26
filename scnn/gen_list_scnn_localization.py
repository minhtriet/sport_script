from itertools import islice
import numpy as np
import sys
import pdb
import os
import json
from subtitle import Subtitle
import random
from event import Event

if (sys.argv[1] != 'fb') and (sys.argv[1] != 'bb'):
  print "gen_list_loc_scnn <fb/bb>"
  sys.exit(1)

WINDOW_SIZE = [16,32,64,128,256,512] 
OVERLAP_RATE = 0.75
ZERO_OUPUT_PROBABILITY = 0.01

def print_data(_file, event):
  _file.write(event.to_string())

with open('../%s_classes.json' % sys.argv[1], 'r') as f:
  classes = json.load(f)
  count = [0] * len(classes)
  events = {k: [] for k in range(len(classes))}

for split in ['train', 'val']:
  for window_size in WINDOW_SIZE:
    FRAME_PATH = "/media/data/mtriet/dataset/%s_frame_%" % (sys.argv[1], split)
    SUB_PATH = "/media/data/mtriet/raw_video/%s/%s" % (sys.argv[1], split)
    for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
      for folder in sub_folder:       
        print folder
        subtitles = Subtitle.load_subtitle(SUB_PATH, folder, sys.argv[3]) 
        frames = sorted(os.listdir(frame_root + '/' + folder))
        sub_index = 0
        sub_class = classes[subtitles[sub_index].klass]            
        for begin_pivot in range(1, len(frames) - window_size, int(window_size*(1 - OVERLAP_RATE))):  # ignore last few frames
            if (begin_pivot > subtitles[sub_index].end) and (sub_index < len(subtitles) - 1):
                sub_index += 1 
                sub_class = classes[subtitles[sub_index].klass]            

            end_pivot = min(begin_pivot + window_size, len(frames))
            segment = range(begin_pivot, begin_pivot + window_size + 1)
            sub_range = subtitles[sub_index].get_range()
            intersection = np.intersect1d(segment, sub_range)
            if len(intersection) == len(segment):        # the subtitle contains the segment
                count[sub_class] += 1
                event = Event(frame_root, folder, begin_pivot, sub_class, window_size, 1.0)
                events[sub_class].append(event)
            else:
                union = len(segment) + len(sub_range) - len(intersection)
                current_score = 1.0 * len(intersection) / union 
                if current_score > 0.7:
                    count[sub_class] += 1
                    event = Event(frame_root, folder, begin_pivot, sub_class, window_size, current_score)
                    events[sub_class].append(event)
                    continue
                else:  # check if next segment has better score, if > 0.7, and if max of them > 0.5
                    if sub_index < len(subtitles) - 1: # not at last subtitle
                        sub_range = subtitles[sub_index+1].get_range()
                        intersection = np.intersect1d(segment, sub_range)
                        next_score = 1.0 * len(intersection) / union 
                        if max(current_score, next_score) > 0.5:
                            count[sub_class] += 1
                            event = Event(frame_root, folder, begin_pivot, sub_class, window_size, max(current_score, next_score))
                            events[sub_class].append(event)
                            continue
                    count[0] += 1
                    event = Event(frame_root, folder, begin_pivot, 0, window_size, 1.0)
                    events[0].append(event)

  print(count)
  median = int(np.median(count))

  with open('scnn_%s_%s_localization.lst' % (sys.argv[1], split) , 'w') as train_file:
    if split == 'train':
      for k in range(len(count)):
        if count[k] > median * 1.5: 
          for s in range(median):
            i = np.random.randint(count[k])
            print_data(_file, events[k][i]) 
        else:
          for s in range(len(events[k])): 
            print_data(_file, events[k][s])
          # oversample and augment
          for s in range(median - len(events[k])): 
            i = np.random.randint(count[k])          
            print_data(_file, events[k][i])
    else:
      for k in range(len(count)):
        for s in range(len(events[k])): 
          print_data(_file, events[k][s])
