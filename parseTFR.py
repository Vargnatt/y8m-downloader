
# pylint: disable = W0312, E0401, C0103, W0611

import csv
import os
import tensorflow as tf


path = "downloader/"
if 'path' in os.environ:
    path = os.environ['path']
filelist = []
featurelist = []
for files in os.listdir(path):
    if files.endswith(".tfrecord"):
        # filelist.append(path+files)
        for example in tf.python_io.tf_record_iterator(path + files):
            result = tf.train.Example.FromString(example)
            dic = {}
            dic["video_id"] = result.features.feature["video_id"].value.byte_list.value[0]
            lst = []
            for i in range(len(result.features.feature["video_id"].value.int64_list.value)):
                lst.append(
                    int(result.features.feature["video_id"].value.int64_list.value[i]))
            dic["labels"] = lst
            featurelist.append(dic)
dict_name = "records.csv"

# thefile = open(dict_name, 'wb')
# with open(dict_name, 'w') as outfile:
#     json.dump(featurelist, outfile)
# f=open(dict_name,'w')
with open(dict_name, 'w') as output:
    writer = csv.writer(output)
    writer.writerows(featurelist)
