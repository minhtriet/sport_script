import itertools
import pdb
import os
import sys
import subprocess
import shutil

# input: vid_path = video path, allows wildcard
# output: folders, each contains all frames of the video
#if sys.argv[2] == 'train':
#  OUTPUT = '/media/data/mtriet/dataset/%s_frames_train/' % sys.argv[1]
#elif sys.argv[2] == 'val':
#  OUTPUT = '/media/data/mtriet/dataset/%s_frame_val/' % sys.argv[1]
#else:
#  print('train or val?')
#  exit(1)

OUTPUT = '/media/data/mtriet/dataset/%s_frame_val/' % sys.argv[1]
def dump_frames(vid_path):
    vid_name = OUTPUT + os.path.basename(vid_path).split('.')[0]
    if os.path.isdir(vid_name):
        shutil.rmtree(vid_name)
    
    os.mkdir(vid_name)
    os.system('ffmpeg -i %s %s/%%05d.jpg' % (vid_path, vid_name))

if __name__ == "__main__":
    print("meant to work with val")
    if os.path.exists(OUTPUT):
      shutil.rmtree(OUTPUT)
    os.makedirs(OUTPUT)

    if len(sys.argv) < 3:
        print 'gen_frame <fb/bb> <path>'
        sys.exit(1) 
    for i in range(2, len(sys.argv)):
        dump_frames(sys.argv[i])
