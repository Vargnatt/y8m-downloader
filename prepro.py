# pylint: disable = W0312, E0401, C0103, W0611
import os
import cv2
import argparse
import multiprocessing


parser = argparse.ArgumentParser()
parser.add_argument('--dst', help='folder to save extracted frames')
parser.add_argument('--src', help='folder contains videos')
# parser.add_argument('--lib',help='opencv or scikit-video')

args = parser.parse_args()
dst_path = args.dst
vid_path = args.src

if not vid_path.endswith('/'):
    vid_path = vid_path + '/'
if not dst_path.endswith('/'):
    dst_path = dst_path + '/'

for files in os.listdir(vid_path):
    vid_dst = dst_path + files
    os.mkdir(vid_dst)
    vidcap = cv2.VideoCapture(vid_path + files)
    fps=vidcap.get()
    stride=int(fps/3)
    count = 0
    success = True
    seq = 0
    while vidcap.isOpened():
        success, image = vidcap.read()
        if count % stride == 0:
            name = '{0:0>5}'.format(seq)
            cv2.imwrite(vid_dst + '/' + name + '.png', image)
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

# Multi Thread
# filelist = os.listdir(vid_path)
# locker = [0] * len(filelist)


# def process(files):
#     vid_dst = dst_path + files
#     os.mkdir(vid_dst)
#     vidcap = cv2.VideoCapture(vid_path + files)
#     count = 0
#     success = True
#     seq = 0
#     while success:
#         success, image = vidcap.read()
#         if count % 10 == 0:
#             name = '{0:0>5}'.format(seq)
#             cv2.imwrite(vid_dst + '/' + name + '.png', image)
#             seq += 1
#         count += 1


# p = multiprocessing.Pool()
# for f in filelist:
#     p.apply_async(process, [f])

# p.close()
# p.join()
