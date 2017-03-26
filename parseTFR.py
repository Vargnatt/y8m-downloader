
# pylint: disable = W0312, E0401, C0103, W0611

import json
import os
import tensorflow as tf


path = "downloader/"
filist = []
if 'path' in os.environ:
    path = os.environ['path']
if 'filist' in os.environ:
    filist = os.environ['filist']

def filtLabel(d):
    if not filter:
        return d
    else:
        d = [x for x in d if x in filist]
        return d


filelist = []
featurelist = []
for files in os.listdir(path):
    if files.endswith(".tfrecord"):
        # filelist.append(path+files)
        for example in tf.python_io.tf_record_iterator(path + files):
            result = tf.train.Example.FromString(example)
            dic = {}
            if hasattr(result, 'context'):
                dic["video_id"] = result.context.feature["video_id"].byte_list.value[0]
                lst = []
                for i in range(len(result.context.feature["video_id"].int64_list.value)):
                    lst.append(
                        int(result.context.feature["video_id"].int64_list.value[i]))
                lst = filtLabel(lst)
                dic["labels"] = lst
            elif hasattr(result, 'features'):
                dic["video_id"] = result.features.feature["video_id"].byte_list.value[0]
                lst = []
                for i in range(len(result.features.feature["video_id"].int64_list.value)):
                    lst.append(
                        int(result.features.feature["video_id"].int64_list.value[i]))
                lst = filtLabel(lst)
                dic["labels"] = lst
            featurelist.append(dic)
dict_name = "records.json"

# thefile = open(dict_name, 'wb')
# with open(dict_name, 'w') as outfile:
#     json.dump(featurelist, outfile)
# f=open(dict_name,'w')
# print(type(featurelist))
# print(len(featurelist))
with open(dict_name, 'w') as output:
    json.dump(featurelist,output)