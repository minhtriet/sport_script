import sys
import os

from subtitle import Subtitle

SUB_PATH = "/media/data/mtriet/raw_video/%s/train" % (sys.argv[1])
FRAME_PATH = "/media/data/mtriet/dataset/scnn_%s_frames" % sys.argv[1]

if __name__ == '__main__':
  if len(sys.argv) > 4 or len(sys.argv) < 3:
    print('command fb/bb front_pad rear_pad')
    sys.exit(0)
  for frame_root, sub_folder, _ in os.walk(FRAME_PATH):
    for folder in sub_folder:
      print(folder)
      subtitles = Subtitle.load_subtitle(SUB_PATH, folder, False)

      with open("%s/%s_pad.aqt" % (SUB_PATH, folder), 'w') as f:
        for s in subtitles:
          f.write(s.to_string(sys.argv[2], sys.argv[3]))
