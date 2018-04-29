# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:50:37 2017

@author: mtriet
"""

import cv2
import pdb
import sys
import glob
import os
import shutil

DATASET_PATH = '/media/data/mtriet/raw_video/%s/eval/' % sys.argv[1]
OUTPUT_PATH = '/media/data/mtriet/dataset/%s_frames_eval_split/' % sys.argv[1]

def create_sub(file_name):
    print file_name
    start = [1]
    end = []
    name = os.path.basename(file_name)
    name = name.split('.')[0]
    os.system('rm %s/*.jpg' % OUTPUT_PATH) 
    os.system('ffmpeg -loglevel panic -i %s %s/%%06d.jpg' % (file_name, OUTPUT_PATH))

    # create subtitle for visualizing
    
    with open(file_name.split('.')[0] + '_auto.aqt', 'w') as f:
      print "Create file %s" % file_name.split('.')[0] + '_auto.aqt'
      count = 1
      if not os.path.isdir("%s_%03d" % (name, count)):
          os.mkdir("%s_%03d" % (name, count))
      filenames = glob.glob('%s/*.jpg' % OUTPUT_PATH)
      filenames.sort()
      for i in xrange(len(filenames)-1):  
          frame = cv2.imread(filenames[i])
          frame1 = cv2.imread(filenames[i+1])
          hist1 = cv2.calcHist([frame],[0],None,[256],[0,256])
          hist2 = cv2.calcHist([frame1],[0],None,[256],[0,256])
          diff = sum(sum(abs(hist1 - hist2)))
          if (diff > 1.5*10**5):
              f.write('-->> %d\n%d\n-->> %d\n\n'% (start[-1], count, i))
              base = i
              count += 1
              start.append(i+1)
              end.append(i)
      end.append(len(filenames))
    # move file to subfolder
    for i in xrange(len(start)):
        current_folder = "%s/%s_%03d" % (OUTPUT_PATH, name, i)
        if os.path.isdir(current_folder):
          shutil.rmtree(current_folder)
        os.mkdir(current_folder)
        os.chdir(current_folder)
        # rename files to 0 range
        for j in xrange(start[i], end[i]+1):
            shutil.move('../%06d.jpg' % j, '%06d.jpg' % (j-start[i]+1))
    os.chdir('..')

for i in glob.glob("%s/*.mp4" % DATASET_PATH):
    create_sub(i)
