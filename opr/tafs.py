# coding: utf-8
import sys
sys.path.append('..')

import os
import time
import json as js
from datetime import datetime
import traceback
import algom.collecter as clt

with open('../config.json') as f:
    config = js.load(f)

LOG_PATH = config['taf']['log_path']
ARCHIVE_PATH = config['taf']['archive_path']
REALTIME_PATH = config['taf']['realtime_path']

import opr.log as log
logger = log.setup_custom_logger(LOG_PATH+'taf','root')


def check_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_json(rpts,pfn):
    js_context = js.dumps(rpts)
    with open(pfn,'w') as f:
        f.write(js_context)


def get_save_name(utcnow):
    return utcnow.strftime('%Y%m%d%H%M')


def main():
    while True:
        utcnow = datetime.utcnow()
        if utcnow.minute in (5,15,25,35,45,55):
            print('{}: start crawling'.format(datetime.utcnow()))
            logger.info(' start crawling')
            tafs = clt.get_rpts(kind='taf')

            pfn = REALTIME_PATH + 'last_taf.json'
            save_json(tafs,pfn)
            print('{}: saved in real time dir'.format(datetime.utcnow()))
            logger.info(' saved in real time dir.')

            today = utcnow.strftime('%Y%m%d')
            check_dirs(ARCHIVE_PATH+today)
            pfn = ARCHIVE_PATH+today+'/'+get_save_name(utcnow)+'.json'
            save_json(tafs,pfn)
            print('{}: saved in archive dir'.format(datetime.utcnow()))
            logger.info(' saved in archive dir.')

            time.sleep(60)
        else:
            print('{}: not process point, delaying'.format(datetime.utcnow()))
            time.sleep(2)

        today = utcnow.strftime('%Y%m%d')

if __name__ == '__main__':
    try:
        main()
    except:
        # 若出现异常，则打印回溯信息并记入日志
        traceback_message = traceback.format_exc()
        print(traceback_message)
        logger.error(traceback_message)
        exit()
