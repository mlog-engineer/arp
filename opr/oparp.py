# coding: utf-8
'''
自动爬取metar或taf报文程序

使用方法
-------
自动爬取 METAR 报文
$ python oparp.py metar

自动爬取 TAF 报文
$ python oparp.py taf
'''
import sys
sys.path.append('..')

import os
import time
import json as js
from datetime import datetime
import traceback
import algom.collecter as clt

kind = sys.argv[1]

with open('../config.json') as f:
    config = js.load(f)

LOG_PATH = config[kind]['log_path']
ARCHIVE_PATH = config[kind]['archive_path']
REALTIME_PATH = config[kind]['realtime_path']

import opr.log as log
logger = log.setup_custom_logger(LOG_PATH+kind,'root')


def check_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_json(rpts,pfn):
    js_context = js.dumps(rpts)
    with open(pfn,'w') as f:
        f.write(js_context)


def get_save_name(utcnow):
    return utcnow.strftime('%Y%m%d%H%M')


def drop_duplication(rpts,kind):
    '''清除与上次扫描相同的报文

    输入参数
    -------
    rpts : `dict`
        从网络上抓取的报文字典，该字典以ICAO码为键，以报文内容为值

    返回值
    -----
    `dict` : 经过与前一时次报文文件的对比，清除了重复（未更新）报文后的报文字典
    '''
    with open(REALTIME_PATH+'all_{}s.json'.format(kind)) as f:
        pre_rpts = js.load(f)

    keys = list(rpts.keys())
    for k in keys:
        if rpts[k] == pre_rpts[k]:
            rpts.pop(k)
        else:
            print('{0}: {1} is updated'.format(datetime.utcnow(),k))
            logger.info(' {} is updated'.format(k))
    return rpts


def update_all(rpts,kind):
    with open(REALTIME_PATH+'all_{}s.json'.format(kind)) as f:
        pre_rpts = js.load(f)
    for k in pre_rpts:
        try:
            if rpts[k] != pre_rpts[k]:
                pre_rpts[k] = rpts[k]
        except KeyError as e:
            pass

    save_json(pre_rpts,REALTIME_PATH+'all_{}s.json'.format(kind))


def main():
    while True:
        utcnow = datetime.utcnow()
        if utcnow.minute in (0,5,15,20,25,30,35,40,45,50,55):
            print('{}: start crawling'.format(datetime.utcnow()))
            logger.info(' start crawling')
            pfn_new = REALTIME_PATH + 'updated_{}s.json'.format(kind)
            pfn_all = REALTIME_PATH + 'all_{}s.json'.format(kind)
            if not os.path.exists(pfn_all):
                icaos = ['ZBAA', 'ZBTJ', 'ZBSJ', 'ZBYN', 'ZBHH', 'ZYTX', 'ZYTL',
                         'ZYCC', 'ZYHB', 'ZSSS', 'ZSPD', 'ZSNJ', 'ZSOF', 'ZSHC',
                         'ZSNB', 'ZSFZ', 'ZSAM', 'ZSQD', 'ZHHH', 'ZHCC', 'ZGHA',
                         'ZGGG', 'ZGOW', 'ZGSZ', 'ZGNN', 'ZGKL', 'ZJHK', 'ZJSY',
                         'ZUCK', 'ZUUU', 'ZPPP', 'ZLXY', 'ZLLL', 'ZWWW', 'ZWSH',
                         'VHHH', 'VMMC', 'ZUGY', 'RCSS', 'RCKH', 'RCTP']
                rpts_init = dict(zip(icaos,['']*len(icaos)))
                save_json(rpts_init,pfn_all)

            rpts_download = clt.get_rpts(kind)
            rpts_new = drop_duplication(rpts_download,kind)

            if rpts_new:
                save_json(rpts_new,pfn_new)
                print('{}: saved in real time dir'.format(datetime.utcnow()))
                logger.info(' saved in real time dir')

                update_all(rpts_download,kind)
                print('{}: updated all record'.format(datetime.utcnow()))
                logger.info(' updated all record')

                today = utcnow.strftime('%Y%m%d')
                check_dirs(ARCHIVE_PATH+today)
                pfn = ARCHIVE_PATH+today+'/'+get_save_name(utcnow)+'.json'
                save_json(rpts_new,pfn)
                print('{}: archived'.format(datetime.utcnow()))
                logger.info(' archived')
            else:
                print('{}: last time is not updated'.format(datetime.utcnow()))
                logger.info(' last time is not updated')

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
