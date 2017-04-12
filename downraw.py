# pylint: disable = W0312, E0401, C0103, W0611, E0401
import glob
import os
import json
import youtube_dl


schedule_dir = "/media/ydl/NewDisk/workspace/y8m/dst/schedule"
listname = "/media/ydl/NewDisk/workspace/y8m/trainlist.txt"
urlist = []


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def splt(lst, s=3000):
    seq = 0
    for i in range(0, len(lst), s):
        tmp = lst[i:i + s]
        name = '{0:0>3}'.format(seq)
        fn = '{}/{}.txt'.format(schedule_dir, name)
        seq += 1
        with open(fn, 'w') as dst:
            for item in tmp:
                dst.write('%s\n' % item)
        dst.close()


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


# split and create schedule if folder empty
#print(not os.listdir(schedule_dir))
if not os.listdir(schedule_dir):
    with open(listname) as f:
        urls = f.read().splitlines()
    f.close()
    splt(urls)
    sch = open('ckpt.json', 'w')
    sch.close()
# read schedule and start from check point
filelist = glob.glob('{}/*.txt'.format(schedule_dir))
ckpt = glob.glob('{}/*.json'.format(schedule_dir))[0]


if os.stat(ckpt).st_size == 0:
    chunk = 0
    entry = 0
else:
    with open('{}/ckpt.json'.format(schedule_dir), 'r') as jsf:
        data = json.load(jsf)
        chunk = data['chunk']
        entry = data['entry']
    jsf.close()

dic = {}
check_e = entry
check_ch = chunk
dl_opts = {
    'outtmpl': '/media/ydl/NewDisk/videos/%(id)s',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'ignoreerrors':True
}

for files in filelist[chunk:-1]:
    if files == filelist[chunk]:
        idx = entry
        check_e = entry
    else:
        idx = 0
        check_e = 0
    dic['chunk'] = check_ch
    f = open(files, 'r')
    lists = f.read().splitlines()

# check point
    for e in lists[idx:-1]:
        # read and down
        with youtube_dl.YoutubeDL(dl_opts) as dl:
            code_no=dl.download([e])
            print(code_no)
        check_e += 1
        dic['entry'] = check_e
        ckf = open('{}/ckpt.json'.format(schedule_dir), 'w')
        json.dump(dic, ckf)
        ckf.close()
    check_ch += 1
