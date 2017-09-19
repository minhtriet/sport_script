import itertools
import pdb
import os
import sys
import subprocess

# input: vid_path = video path, allows wildcard
# output: folders, each contains all frames of the video
def dump_frames(vid_path):
    vid_name = os.path.basename(vid_path).split('.')[0]
    subtitle_path = os.path.dirname(vid_path) + '/' + vid_name + ".aqt"

    try:
        os.mkdir(vid_name)
    except OSError:
        print '%s existed!' % vid_name
        #return
    
    os.system('ffmpeg -i %s %s/%%05d.jpg' % (vid_path, vid_name))
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
                os.mkdir(vid_name + '/' + sub_folder + '/')
            except:
                print '%s existed!' % sub_folder
                continue

            for value in range(next_n_lines[0], next_n_lines[2]):
                try:
                    os.rename("%s/%05d.jpg" % (vid_name, value), "%s/%s/%05d.jpg" % (vid_name, sub_folder, value))
                except:
                    dup_frame = subprocess.check_output(['/usr/bin/find', vid_name, '-name', '%05d.jpg' % value]).strip()
                    if '_bg' in sub_folder:
                        if '_bg' in dup_frame:
                            # conflict with background
                            print 'Conflict with background, ignoring current frame. %s' % sub_folder 
                            os.rmdir(vid_name + '/' + sub_folder)
                            break
                        else:
                            # conflict with a class                            
                            print 'Conflict with a class at %s, stoping %s' % (dup_frame, sub_folder)
                            os.rmdir(vid_name + '/' + sub_folder)
                            break
                    else:
                        if '_bg' in dup_frame:
                            # move frames from bg_sub_folder to this sub_folder
                            os.rename(dup_frame, "%s/%s/%05d.jpg" % (vid_name, sub_folder, value))
                        else:
                            pdb.set_trace()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'gen_frame <path>, note that they should be accompanied by aqt subtitle'
        sys.exit(1) 
    for i in range(1, len(sys.argv)):
        dump_frames(sys.argv[i])
    
