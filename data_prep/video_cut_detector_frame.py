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
import pdb

DATASET_PATH = '/media/data/mtriet/raw_video/%s_eval/' % sys.argv[1]
OUTPUT_PATH = '/media/data/mtriet/raw_video/%s_eval_split/' % sys.argv[1]

def create_sub(file_name):
    start = [0]
    end = []
    name = os.path.basename(file_name)
    name = name.split('.')[0]
    folder = OUTPUT_PATH + name
     
    try:
      os.mkdir(folder)
      os.system('ffmpeg -i %s %s/image_%%05d.jpg' % (file_name, folder))
    except:
      return # video has been done

    # create subtitle for visualizing
    f = open(file_name.split('.')[0] + '_auto.aqt', 'w')
    print "Create file %s" % file_name.split('.')[0] + '.aqt'
    base = 0
    count = 1
    os.mkdir("%s/%s_%03d" % (folder, name, count))
    for dirname, dirnames, filenames in os.walk(folder):
        filenames.sort()
        for i in xrange(len(filenames)-1):  
            frame = cv2.imread("%s/%s" % (dirname, filenames[i]))
            frame1 = cv2.imread("%s/%s" % (dirname, filenames[i+1]))
            hist1 = cv2.calcHist([frame],[0],None,[256],[0,256])
            hist2 = cv2.calcHist([frame1],[0],None,[256],[0,256])
            
            diff = sum(sum(abs(hist1 - hist2)))
            if (diff > 3*10**5):
                f.write('-->> %d\n%d\n-->> %d\n\n'% (base, count, i))
                base = i
                count += 1
                start.append(i+1)
                end.append(i)
    end.append(i)

    # move file to subfolder
    for i in xrange(len(start)):
        current_folder = "%s/%s_%03d" % (folder, name, i)
        if not os.path.isdir(current_folder):
            os.mkdir(current_folder)
        os.chdir(current_folder)
        os.system('mv ../{%05d..%05d}.jpg %s/%s/{%05d..%05d}.jpg' % (start[i], end[i]-1, 1, end[i] - start[i]))
                

for i in glob.glob("%s/*.mp4" % DATASET_PATH):
    create_sub(i)
