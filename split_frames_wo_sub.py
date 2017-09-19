import itertools
import pdb
import os
import sys
import subprocess

# input: vid_path = video path, allows wildcard
# output: folders, each contains all frames of the video
def dump_frames(vid_path, overwrite):
    vid_name = os.path.basename(vid_path).split('.')[0]
    if os.path.isdir(vid_name):
        if int(overwrite) == 1:
            os.rmdir(vid_name)
        else:
            return
    os.mkdir(vid_name)
    os.system('ffmpeg -i %s %s/%%05d.jpg' % (vid_path, vid_name))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'gen_frame <path> overwrite(0/1)'
        sys.exit(1) 
    for i in range(1, len(sys.argv)-1):
        dump_frames(sys.argv[i], sys.argv[len(sys.argv)-1])
    
