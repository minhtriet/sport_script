# after extracting the flow, use this file to split the frames to appropirate folders
# gen_list_tsn next

import itertools
import pdb
import os
import sys
import shutil

# input: vid_path = video path, allows wildcard
# output: folders, each contains all frames of the video
def dump_frames(sport, pad):
  VID_PATH = "/media/data/mtriet/raw_video/%s/train/" % sport
  OUTPUT = '/media/data/mtriet/dataset/tsn_%s_frames/' % sport
  ORIGINAL_FRAMES = '/media/data/mtriet/dataset/backup/tsn_%s_frames/train/' % sport

  for f in os.listdir(VID_PATH):
    if f.endswith(".aqt"):
      if (pad and f.endswith('_pad.aqt')) or (not pad and not f.endswith('_pad.aqt')):
        vid_name = f[:-4] if not pad else f[:-8]  # remove extension
        subtitle_path = os.path.dirname(VID_PATH) + '/' + f
        with open(subtitle_path, 'r') as f:
          index = 0
          while True:
            index = index + 1
            next_n_lines = list(itertools.islice(f, 4))
            if not next_n_lines:
              break
            next_n_lines[0] = int(next_n_lines[0].split(' ')[1])
            next_n_lines[2] = int(next_n_lines[2].split(' ')[1])
            sub_folder = '_'.join([vid_name, str(index), next_n_lines[1].strip()])
            output_frame_path = OUTPUT + '/' + sub_folder + '/'
            try:
              os.mkdir(output_frame_path)
            except:
              shutil.rmtree(output_frame_path)
              os.mkdir(output_frame_path)

            for num, value in enumerate(range(next_n_lines[0], next_n_lines[2])):
              shutil.copyfile("%s/%s/flow_x_%05d.jpg" % (ORIGINAL_FRAMES, vid_name, value), "%s/flow_x_%05d.jpg" % (output_frame_path, num))
              shutil.copyfile("%s/%s/flow_y_%05d.jpg" % (ORIGINAL_FRAMES, vid_name, value), "%s/flow_y_%05d.jpg" % (output_frame_path, num))
              shutil.copyfile("%s/%s/image_%05d.jpg" % (ORIGINAL_FRAMES, vid_name, value), "%s/image_%05d.jpg" % (output_frame_path, num))

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print 'gen_frame <sport> <pad (T/F)>'
    sys.exit(1)
  dump_frames(sys.argv[1], sys.argv[2])
