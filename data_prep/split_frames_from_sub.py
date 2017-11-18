import glob
import itertools
import pdb
import os
import sys
import subprocess

OUTPUT = '/media/data/mtriet/dataset/%s_frames/' % sys.argv[1]
VIDEO_PATH = '/media/data/mtriet/raw_video/%s/train/*.mp4' % sys.argv[1]
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
        print '%s existed!' % output_path
    
   # os.system('ffmpeg -i %s -vf scale=640:360 %s/%%05d.jpg' % (output_path, vid_name))
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

            try:
                os.mkdir(output_path + '/' + sub_folder + '/')
            except:
                print '%s existed!' % (output_path + '/' + sub_folder + '/')

            for num, value in enumerate(range(next_n_lines[0], next_n_lines[2])):
                try:
                    os.rename("%s/%05d.jpg" % (output_path, value), "%s/%s/%05d.jpg" % (output_path, sub_folder, num))
                except:
                    dup_frame = subprocess.check_output(['/usr/bin/find', output_path, '-name', '%05d.jpg' % value]).strip()
                    if '_bg' in sub_folder:
                        if '_bg' in dup_frame:
                            # conflict with background
                            print 'Conflict with background, ignoring current frame. %s' % sub_folder 
                            os.rmdir(output_path + '/' + sub_folder)
                            break
                        else:
                            # conflict with a class                            
                            print 'Conflict with a class at %s, stoping %s' % (dup_frame, sub_folder)
                            os.rmdir(output_path + '/' + sub_folder)
                            break
                    else:
                        if '_bg' in dup_frame:
                            # move frames from bg_sub_folder to this sub_folder
                            os.rename(dup_frame, "%s/%s/%05d.jpg" % (output_path, sub_folder, value))
                        else:
                            print "%s %s" % (dup_frame, sub_folder)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print 'gen_frame <sport>'
    sys.exit(1) 
  
  for i in glob.glob(VIDEO_PATH):
    dump_frames(i) 
