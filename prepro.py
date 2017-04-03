# pylint: disable = W0312, E0401, C0103, W0611
import os
import cv2


vid_path = ''
dst_path = ''

for files in os.listdir(vid_path):
    vid_dst = dst_path + files
    os.mkdir(vid_dst)
    vidcap = cv2.VideoCapture(vid_path + files)
    count = 0
    success = True
    seq = 0
    while success:
        success, image = vidcap.read()
        if count % 10 == 0:
            name = '{0:0>5}'.format(seq)
            cv2.imwrite(vid_dst+'/'+name, image)
            seq += 1
        count += 1

# vidcap = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
# success, image = vidcap.read()
# count = 0
# success = True
# while success:
#     success, image = vidcap.read()
#     print('Read a new frame: ', success)
#     cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
#     count += 1
