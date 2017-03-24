
# pylint: disable = W0312, E0401, C0103, W0611

import json
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
            featurelist.append(result)
dict_name = "records.json"

with open(dict_name, 'w') as outfile:
    json.dump(featurelist, outfile)
