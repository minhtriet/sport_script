import pdb
import os

FRAME_PATH = "/media/data/mtriet/dataset/fb_frames_scnn_localization"
for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
    for folder in sub_folder:        
        frames = os.listdir(frame_root + '/' + folder)
        with open('%s.aqt' % folder, 'r') as f:
            os.path.listdir(folder)
            pdb.set_trace() 
