import os

os.system('ffmpeg -i %s -vf scale=640:360 %s/%%05d.jpg' % (vid_path, output_path))
