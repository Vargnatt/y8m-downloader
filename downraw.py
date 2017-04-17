
# coding: utf-8

# In[1]:

# pylint: disable = W0312, E0401, C0103, W0611, E0401
import glob
import os
import sys
import json
import youtube_dl
from youtube_dl.utils import *
from cStringIO import StringIO

erf = open('errlist.json', 'r')
errKeyWords = json.load(erf)
erf.close()

schedule_dir = "/media/ydl/NewDisk/workspace/y8m/dst/schedule"
listname = "/media/ydl/NewDisk/workspace/y8m/trainlist.txt"
urlist = []


# In[2]:

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class MyLogger(object):
    def __init__(self):
        self.m = ''

    def debug(self, msg):
        self.m = ''
        pass

    def warning(self, msg):
        self.m = ''
        pass

    def error(self, msg):
        print(msg)
        self.m = msg

    def getMessage(self):
        return self.m


def splt(lst, s=1000):
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


# In[3]:

def customdl(dler, url):
    try:
            # It also downloads the videos
        res = dler.extract_info(
            url, force_generic_extractor=dler.params.get('force_generic_extractor', False))
    except UnavailableVideoError:
        #         print('test point')
        #         dler.report_error('unable to download video')
        raise
    except MaxDownloadsReached:
        dler.to_screen('[info] Maximum number of downloaded files reached.')
        raise
    else:
        if dler.params.get('dump_single_json', False):
            dler.to_stdout(json.dumps(res))


# In[4]:

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
logger = MyLogger()
dl_opts = {
    'outtmpl': '/media/ydl/NewDisk/videos/%(id)s',
    'logger': logger,
    'progress_hooks': [my_hook],
    'ignoreerrors': True
}

failed = open('failedlist.txt', 'a')
# In[5]:

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
    breakflag = True
# check point
    for e in lists[idx:-1]:
        # read and down
        #         with Capturing() as output:
        with youtube_dl.YoutubeDL(dl_opts) as dl:
            code = dl.download([e])
#             customdl(dl,e)
#             if len(output)>0 and output[-1].find('504'):
#                 print('fuckyoutube')
            if not code == 0:
                msg = logger.getMessage()
                failed.write(e + '\n')
                if any(k in msg for k in errKeyWords):
                    print('Network Down and Quit')
                    break
        check_e += 1
        dic['entry'] = check_e
        ckf = open('{}/ckpt.json'.format(schedule_dir), 'w')
        json.dump(dic, ckf)
        ckf.close()
    else:
        check_ch += 1
        continue
    break

failed.close()

