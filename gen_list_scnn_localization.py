# train proposal network.
# material used: Section 3.2 of http://dvmmweb.cs.columbia.edu/files/dvmm_scnn_paper.pdf

# split all frames, for every 8 frames, (1-8, 9-16, ...) calculate IoU with the ground truth
# score = action or not

WINDOW_SIZE = 8

def dump_frames(vid_path):
    vid_name = vid_path.split('/')[-1].split('.')[0]
    out_full_path = vid_name + '_all_frames'
    try:
        os.mkdir(out_full_path)
    except OSError:
        pass
    print 'ffmpeg -i %s %s/%%05d.jpg' % (vid_path, out_full_path)
    os.system('ffmpeg -i %s %s/%%05d.jpg' % (vid_path, out_full_path))
    
    # read the subtitle
    
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'gen_frame <path>'
        sys.exit(1) 
    for i in range(1, len(sys.argv)):
        dump_frames(sys.argv[i])
    
