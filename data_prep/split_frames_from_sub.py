import glob
import itertools
import pdb
import os
import sys
import subprocess
import shutil

if sys.argv[2] == 'train':
  OUTPUT = '/media/data/mtriet/dataset/%s_frames/' % sys.argv[1]
elif sys.argv[2] == 'eval':
  OUTPUT = '/media/data/mtriet/dataset/%s_frames_eval/' % sys.argv[1]

VIDEO_PATH = '/media/data/mtriet/raw_video/%s/%s/*.mp4' % (sys.argv[1], sys.argv[2])
# input: vid_path = video path, allows wildcard
# output: folders, each contains all frames of the video
def dump_frames(vid_path):
    vid_name = os.path.basename(vid_path).split('.')[0]
    subtitle_path = os.path.dirname(vid_path) + '/' + vid_name + ".aqt"
    output_path = OUTPUT + vid_name
    if not os.path.isfile(subtitle_path):
      print '%s not found' % subtitle_path
      return

    try:
      os.mkdir(output_path)
    except OSError:
      print 'cannot create %s!' % output_path
      return
    
    os.system('ffmpeg -i %s -vf scale=640:360 %s/%%05d.jpg' % (vid_path, output_path))
    index = 0

    with open(subtitle_path, 'r') as f:
        while True:
            index = index + 1
            next_n_lines = list(itertools.islice(f, 4))
            if not next_n_lines:
                break
            
            next_n_lines[0] = int(next_n_lines[0].split(' ')[1])
            next_n_lines[2] = int(next_n_lines[2].split(' ')[1])
            sub_folder = '_'.join([vid_name,str(index),next_n_lines[1].strip()])
            output_frame_path = OUTPUT + '/' + sub_folder + '/' 

            try:
                os.mkdir(output_frame_path)
            except:
                print 'cannot create %s!' % output_frame_path 
                return

            for num, value in enumerate(range(next_n_lines[0], next_n_lines[2])):
              try:
                os.rename("%s/%05d.jpg" % (output_path, value), "%s/%05d.jpg" % (output_frame_path, num))
              except:
                continue 

    # delete jpg files left
    shutil.rmtree(output_path)
 
if __name__ == "__main__":
  if len(sys.argv) < 3:
    print 'gen_frame <sport> <train/val>'
    sys.exit(1) 
  
  for i in glob.glob(VIDEO_PATH):
    dump_frames(i) 
