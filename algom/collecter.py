# coding: utf-8
import sys
sys.path.append('..')

import urllib.request
import urllib.parse
import os
import random
import json as js
import time
from datetime import datetime
import logging

with open('../config.json') as f:
    config = js.load(f)

LOG_PATH = config['metar']['log_path']
logger = logging.getLogger('root')

# 目前在AWC中可以查询到的机场范围
icaos = ['ZBAA', 'ZBTJ', 'ZBSJ', 'ZBYN', 'ZBHH', 'ZYTX', 'ZYTL', 'ZYCC', 'ZYHB',
         'ZSSS','ZSPD', 'ZSNJ', 'ZSOF', 'ZSHC', 'ZSNB', 'ZSFZ', 'ZSAM', 'ZSJN',
         'ZSQD', 'ZHHH', 'ZHCC', 'ZGHA', 'ZGGG', 'ZGOW', 'ZGSZ', 'ZGNN', 'ZGKL',
         'ZJHK', 'ZJSY', 'ZUCK','ZUUU', 'ZPPP', 'ZLXY', 'ZLLL', 'ZWWW', 'ZWSH',
         'VHHH', 'VMMC', 'ZUGY', 'RCSS','RCKH', 'RCTP']


def get_rpt_from_awc(icao,kind='metar'):
    '''按机场ICAO码获取报文，数据来自 AWC: https://aviationweather.gov/

    输入参数
    -------
    icao : `str`
        所要查询的机场ICAO码，如'ZBAA'、'ZUUU'
    kind : `str`
        报文类型，须在'metar'和'taf'中选择，默认为'metar'

    返回值
    -----
    `str` : 目标机场最新的航空报文

    示例
    ---
    >>> from collecter import get_rpt_from_awc
    >>> get_rpt_from_awc('ZBAA','metar')
    'METAR ZBAA 030400Z 03005MPS 340V070 CAVOK 07/M21 Q1026 NOSIG'
    '''
    def random_header():
        header_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1)'\
                ' Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv2.0.1) '\
                'Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) '\
                'Presto/2.8.131 Version/11.11',
            'Opera/9.80 (Windows NT 6.1; U; en) '\
                'Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) '\
                'AppleWebKit/535.11 (KHTML, like Gecko) '\
                'Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) '\
                'Gecko/20100101 Firefox/57.0'
              ]
        return random.choice(header_list)

    def get_url(icao,kind):
        if kind == 'metar':
            return 'https://aviationweather.gov/metar/data?ids='+icao
        elif kind == 'taf':
            return 'https://aviationweather.gov/taf/data?ids='+icao

    def save_web(req,savepfn):
        try:
            web_code = urllib.request.urlopen(req).read()
        except Exception as e:
            print('{0}: error: {1}'.format(datetime.utcnow(),e))
            logger.error('error: '+e)
        with open(savepfn,'wb') as fh:
            fh.write(web_code)

    def parse_rpt(pfn,kind='metar'):
        with open(pfn) as f:
            content = f.readlines()
        if kind == 'metar':
            start_index = -1
            end_index = -1
            for n,line in enumerate(content):
                if line.strip() == '<!-- Data starts here -->':
                    start_index = n
                if line.strip() == '<!-- Data ends here -->':
                    end_index = n
            if end_index - start_index == 1:
                rpt = None
            else:
                rpt = content[start_index+1].strip()[6:-12]
        elif kind == 'taf':
            rpt = None
            for n, line in enumerate(content):
                try:
                    line.index(icao+' ')
                except ValueError:
                    pass
                else:
                    rpt = content[n].strip()[6:-12]

        return rpt

    url = get_url(icao,kind)
    req = urllib.request.Request(url)
    header = random_header()
    req.add_header('User-Agent',header)
    save_web(req,'./{}.html'.format(kind))
    rpt = parse_rpt('./{}.html'.format(kind),kind)
    if rpt and kind == 'metar':
        rpt = ' '.join([kind.upper(),rpt])
    try:
        rpt = rpt.replace('<br/>&nbsp;&nbsp;','')
    except AttributeError:
        pass
    os.remove('./{}.html'.format(kind))
    return rpt


def get_rpts(kind='metar'):
    '''批量获取航空报文

    输入参数
    -------
    kind : `str`
        报文类型，可供选择的选项为:'metar'和'taf'

    返回值
    -----
    `dict` : 以ICAO码为键，以报文内容为值的字典
    '''
    rpts = {}
    total = len(icaos)
    for n,icao in enumerate(icaos):
        rpt = get_rpt_from_awc(icao,kind=kind)
        if rpt:
            rpts[icao] = rpt
        print('{0}: ({2}/{3}) {1}'.format(datetime.utcnow(),
                                                  icao,n+1,total))
        logger.info('  ({1}/{2}) {0}'.format(icao,n+1,total))
        time.sleep(2)
    return rpts


if __name__ == '__main__':
    get_rpt_from_awc('ZBAA',kind='metar')
