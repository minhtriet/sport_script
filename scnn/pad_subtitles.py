from subtitle import Subtitle
import sys
import os

SUB_PATH = "/media/data/mtriet/raw_video/%s/%s" % (sys.argv[1], sys.argv[2])
FRAME_PATH = "/media/data/mtriet/dataset/scnn_%s_frames" % sys.argv[1]

if __name__ == '__main__':
  if len(sys.argv) > 5 or len(sys.argv) < 5:
    print('command fb/bb train/val front_pad rear_pad')
    sys.exit(0)
  front_pad = sys.argv[3]
  rear_pad = sys.argv[4]
  for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
    for folder in sub_folder:
      print(folder)
      subtitles = Subtitle.load_subtitle(SUB_PATH, folder, False)

      with open("%s/%s_pad.aqt" % (SUB_PATH, folder), 'w') as f:
        for s in subtitles:
          f.write(s.to_string(sys.argv[3], sys.argv[4]))
