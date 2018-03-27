from itertools import islice
import numpy as np
import sys
import pdb
import os
import json
from subtitle import Subtitle
import random
from event import Event

if (sys.argv[1] == 'fb') or (sys.argv[1] == 'bb'):
  SUB_PATH = "/media/data/mtriet/raw_video/%s/train" % sys.argv[1]
  FRAME_PATH = "/media/data/mtriet/dataset/scnn_%s_frames" % sys.argv[1]
  SUB_PATH = "/media/data/mtriet/raw_video/%s/train" % (sys.argv[1]) 
  TRAIN_VAL_SPLIT = 0.7
else:
  print "gen_list_loc_scnn <fb/bb> <train/eval>"
  sys.exit(1)

WINDOW_SIZE = [16,32,64,128,256,512] 
OVERLAP_RATE = 0.75
ZERO_OUPUT_PROBABILITY = 0.01


def read_next_lines(f, n):
    # read n lines from subtitle and pre-process
    while True:        
        next_n_lines = list(islice(f, n))
        if not next_n_lines:
            return False
        if next_n_lines[1] != 'bg\n':
            break
    next_n_lines[0] = int(next_n_lines[0].split(' ')[1])
    next_n_lines[1] = next_n_lines[1].strip()
    next_n_lines[2] = int(next_n_lines[2].split(' ')[1])
    if (next_n_lines[1] == 'fkwg') or (next_n_lines[1] == 'fkwog'):
        next_n_lines[1] = 'fk'
    if (next_n_lines[1] == 'pkwg') or (next_n_lines[1] == 'pkwog'):
        next_n_lines[1] = 'pk'
    return next_n_lines

def load_subtitle(folder):
    subtitles = []
    with open('%s/%s.aqt' % (SUB_PATH, folder), 'r') as f:
        while True:
            lines = read_next_lines(f, 4)
            if lines:
                sub = Subtitle(lines[1], lines[0], lines[2])
                subtitles.append(sub)
            else:
                break
    return subtitles

def print_data(train_file, val_file, event, mirror):
  if random.random() < TRAIN_VAL_SPLIT: 
    train_file.write(event.to_string(mirror))
  else:
    val_file.write(event.to_string(mirror))

with open('../%s_classes.json' % sys.argv[1], 'r') as f:
  classes = json.load(f)
  count = [0] * len(classes)
  events = {k: [] for k in range(len(classes))}

for window_size in WINDOW_SIZE:
  for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
    for folder in sub_folder:       
      print folder
      subtitles = load_subtitle(folder) 
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

median = int(np.median(count))
with open('scnn_%s_train_localization.lst' % sys.argv[1], 'w') as train_file:
  with open('scnn_%s_val_localization.lst' % sys.argv[1], 'w') as val_file:
    for k in range(len(count)):
      if count[k] > median: 
        for i in range( median):
          i = np.random.randint(count[k])
          print_data(train_file, val_file, events[k][i], False) 
      elif count[k] > median*0.5:
        for s in range(median): 
          i = np.random.randint(count[k])
          print_data(train_file, val_file, events[k][i], False)
          if s < median - count[k]: # augment data for the first median - count[k]
            print_data(train_file, val_file, events[k][i], True)
      else:
        # oversample and augment
        for s in range(median / 2): 
          i = np.random.randint(count[k])          
          print_data(train_file, val_file, events[k][i], False)
          print_data(train_file, val_file, events[k][i], True)
