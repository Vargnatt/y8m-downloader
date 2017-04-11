# pylint: disable = W0312, E0401, C0103, W0611, E0401
import glob
import os
import json
import youtube_dl


schedule_dir = "F:/workspace/y8m/dloader/tmp"
listname = "F:/workspace/y8m/vallist.txt"
urlist = []


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


# split and create schedule if folder empty
if os.listdir(schedule_dir) == "":
    with open(listname) as f:
        urls = f.read().splitlines()
    f.close()
    splt(urls)
    sch = open('ckpt.csv', 'w')
    sch.close()
# read schedule and start from check point
filelist = glob.glob('{}/*.txt'.format(schedule_dir))
ckpt = glob.glob('{}/*.csv'.format(schedule_dir))[0]


if os.stat(ckpt).st_size == 0:
    chunk = 0
    entry = 0
else:
    with open('{}/ckpt', 'r') as jsf:
        data = json.load(jsf)
        chunk = data['chunk']
        entry = data['entry']
    jsf.close()

dic = {}
with open('{}/ckpt', 'w') as ckf:
    for files in filelist[chunk:-1]:
        if files == filelist[chunk]:
            idx = entry
        else:
            idx = 0
        check_e = idx
        check_ch = chunk
        dic['chunk'] = check_ch
        dic['entry'] = check_e
        f = open('{}/{}'.format(schedule_dir, files), 'r')
        lists = f.read().splitlines()

# check point
        for e in lists[idx:-1]:
            # read and down
            dl = {}
            with youtube_dl.YoutubeDL(ydl_opts) as dl:
                dl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
            check_e += 1
            json.dump(dic, ckf)

        check_ch += 1


