#!/usr/bin/python
import os, time
from datetime import datetime, timedelta
from conf import Config

subdomain_folder = Config.SITE_ROOT_FOLDER + Config.MODEL_PATH
dirs = os.listdir(subdomain_folder)
past = datetime.now() - timedelta(days=1)
time_diff = time.mktime(past.timetuple())

for directory in dirs:
    mtime = os.path.getmtime(  + directory)
    if mtime < time_diff:
        os.system("chmod 777 "+ subdomain_folder + directory)
        os.system("rm -rf " + subdomain_folder + directory)
        print time.ctime() + ": deleted folder " + directory

