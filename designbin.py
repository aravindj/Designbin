#!/usr/bin/python
#The one and only file which handles file uploads and assign subdomain.
# author    :   Aravind J
# email     :   aravindkumar.leo@gmail.com
#

from bottle import *
from datetime import *
import json, logging, hashlib, subprocess, os, time
import logging.handlers
from conf import Config

logger = logging.getLogger('designbin')
handler = logging.handlers.RotatingFileHandler(Config.LOGGER_PATH, maxBytes = 10000000,
    backupCount = 25)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@get('/')
def index():
    if is_site_root():
        response.set_cookie("subdomain", str(get_subdomain()))
        return static_file("index.html", root=Config.STATIC_PATH)
    else:
        (scheme, host, path, query_string, fragment) = request.urlparts
        subdomain = host.split('.')[0]
        files = os.listdir(Config.MODEL_PATH + subdomain)
        file_list = []
        for each_file in files:
            url = request.url + "/" + each_file
            file_list.append({'url' : url, 'filename' : each_file})
        return template(Config.STATIC_PATH + "subdomain_index.html", files = file_list)

@get('/:filename')
def get_user_design(filename):
    if is_site_root():
        folder = Config.STATIC_PATH
        return static_file(filename, root=folder)
    else:
        (scheme, host, path, query_string, fragment) = request.urlparts
        subdomain = host.split('.')[0]
        folder = Config.MODEL_PATH + subdomain + "/"
        return static_file(filename, root=folder)

@get('/:folder/:filename')
def render_static_content(folder, filename):
    if is_site_root():
        root = Config.STATIC_PATH + "/" + folder + "/"
        return static_file(filename, root=root)
    else:
        abort(404, "Invalid Url!")

def is_site_root():
    (scheme, host, path, query_string, fragment) = request.urlparts
    if host not in Config.SITE_ROOT:
        return False
    return True

@route("/upload", method = 'POST')
def upload():
    logger = logging.getLogger('designbin')
    result = []
    if is_site_root():
        data = request.POST.get(u'files[]')
        subdomain = request.get_cookie("subdomain")
        response.set_cookie("subdomain", str(subdomain))
        response.content_type = "application/json"
        logger.info("upload(): POST['subdomain'] = %s"% subdomain)
        if is_subdomain_available(subdomain):
            output = os.system("mkdir %s%s"%(Config.MODEL_PATH, subdomain) )
            
        raw = data.value
        logger.info("len(raw) : %s "% str(len(raw)))
        filename = data.filename
        if len(raw) > 2000000:
            result.append({"name":data.filename, 
                   "size":len(raw), 
                   "error":"File too big!"})
        filetype = filename.split('.')[1].lower()
        logger.info("filetype : %s "% filetype)
        if filetype not in ['html', 'css', 'js', 'jpg', 'jpeg', 'png', 'gif']:
            result.append({"name":data.filename, 
                   "size":len(raw), 
                   "error":"File type not supported"})
        logger = logging.getLogger('designbin')
        logger.info("Received File : %s "% data.filename)
        fp = open(Config.MODEL_PATH + subdomain + "/" + filename, "w+")
        fp.write(raw)
        fp.close()
        result.append({"name":data.filename, 
                   "size":len(raw), 
                   "url": "http://%s.%s/%s"% (subdomain, Config.TOP_LEVEL_DOMAIN, data.filename), 
                   "thumbnail_url": "",
                   "delete_url":"", 
                   "delete_type":"POST"})
        return json.dumps(result)
    else:
        logger.warning("upload(): error")
        abort(404, "Invalid Url!")

def get_subdomain():
    while True:
        subdomain = get_hash()
        if is_subdomain_available(subdomain):
            logger.info("get_subdomain(): Generated subdomain - %s"% subdomain)
            return subdomain


def is_subdomain_available(subdomain):
    output = subprocess.check_output(['ls', Config.MODEL_PATH])
    available_folders = output.split('\n')
    if subdomain in available_folders:
        logger.info("subdomain %s not available"% subdomain)
        return False
    return True

def get_hash():
    """Create an md5 hash with current time and client's ip 
    as input and return its 1st 8 chars.
    """
    #Use client's ip and time.time to inject enough randomness
    #Assumption is that 2 requests on exactly the same time and with same ip
    #will not arrive.
    now = str(time.time())
    ip = str(request.get('REMOTE_ADDR'))
    result = hashlib.md5(now + ip).hexdigest()[:8]
    return result

@error(404)
def error404(error):
    return static_file("404.html", root=Config.STATIC_PATH)
