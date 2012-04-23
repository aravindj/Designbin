#!/usr/bin/python
import os, time
from datetime import datetime, timedelta
from conf import Config

dirs = os.listdir(Config.SITE_ROOT_FOLDER + Config.MODEL_PATH)
past = datetime.now() - timedelta(days=10)
time_diff = time.mktime(past.timetuple())

for directory in dirs:
    mtime = os.path.getmtime(Config.MODEL_PATH  + directory)
    if mtime < time_diff:
        os.system("chmod 777 "+ Config.MODEL_PATH + directory)
        os.system("rm -rf " + Config.MODEL_PATH + directory)

