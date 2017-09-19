# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:45:14 2017

@author: mtriet
"""


import sys
import re
import os
import pdb
import datetime

BACKGROUND_STR = 'bg'

if len(sys.argv) < 2:
    sys.stderr.write('Enter video name ')
    sys.exit(1)
elif len(sys.argv) < 3:
    sys.stderr.write('Test: 0, Add 1s before: 1')
    sys.exit(1)

file_name = sys.argv[1]
output = 0

with open(file_name.split('.')[0] + '.srt') as f:
    new_folder = os.path.basename(file_name).split('.')[0]
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    while True:
        f.readline()
        time = f.readline()
        text = f.readline().strip()
        if (not text):
            f.readline()
            continue
        else:
            output = output + 1
            start = time.split("-->")[0].strip().replace(',', '.')
            end = time.split("-->")[1].strip().replace(',', '.')
            
            dt_start = re.split('[:.]', start)
            dt_start = [int(i) for i in dt_start]
            dt_end = re.split('[:.]', end)
            dt_end = [int(i) for i in dt_end]

            # add 1 second before start
            dt_start = datetime.datetime(1,1,1,dt_start[0],dt_start[1],dt_start[2],dt_start[3]) - datetime.datetime(1,1,1,0,0,int(sys.argv[2]))
            dt_end = datetime.timedelta(0, dt_end[2], 0, dt_end[3] ,dt_end[1],dt_end[0],0)
            print("ffmpeg -v verbose -y -r 25 -ss %s -i %s -vcodec copy -acodec copy -t %s %s.mp4" % (start, file_name, (dt_end - dt_start).total_seconds(), os.path.join(new_folder, new_folder + '_' + str(output)+ '_' + text)))
#            os.system("ffmpeg -v verbose -y -r 25 -ss %s -i %s -vcodec copy -acodec copy -t %s %s.mp4" % (start, file_name, (dt_end - dt_start).total_seconds(), os.path.join(new_folder, new_folder + '_' + str(output)+ '_' + text)))
            os.system("ffmpeg -v verbose -y -r 25 -ss %s -i %s -vcodec copy -acodec copy -t %s %s.mp4" % (start, file_name, (dt_end - dt_start).total_seconds(), os.path.join(new_folder, new_folder + '_' + str(output)+ '_' + text)))
        f.readline()

f.close()
