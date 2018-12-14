# coding: utf-8
import sys
import urllib.request
import urllib.parse
import os
import random
import json as js
import time
import re
from datetime import datetime
import logging


logger = logging.getLogger('root')


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
        url = 'https://aviationweather.gov/adds/'\
              'dataserver_current/httpparam?'\
              'dataSource={0}s&requestType=retrieve&format=xml'\
              '&stationString={1}&hoursBeforeNow=2'\
              '&mostRecent=true'.format(kind,icao)
        return url

    def get_web_code(url):
        req = urllib.request.Request(url)
        header = random_header()
        req.add_header('User-Agent',header)
        try:
            web_code = urllib.request.urlopen(req).read().decode('utf-8')
        except KeyboardInterrupt:
            exit()
        except:
            web_code = None
        return web_code


    def parse_rpt(web_code,kind='metar'):
        metar_pattern = '[A-Z]{4} \d{6}Z [0-9A-Z\s/]+'
        taf_pattern = 'TAF [A-Z]{4} \d{6}Z[0-9A-Z\s/]+'
        if kind == 'metar':
            try:
                rpt = 'METAR '+re.search(metar_pattern,web_code).group()
            except AttributeError:
                rpt = None
        elif kind == 'taf':
            try:
                rpt = re.search(taf_pattern,web_code).group()
            except AttributeError:
                rpt = None

        return rpt

    url = get_url(icao,kind)
    web_code = get_web_code(url)
    if web_code:
        rpt = parse_rpt(web_code,kind)
    else:
        rpt = None

    return rpt


def get_rpts(icaos,kind='metar'):
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
            print('{0}: ({2}/{3}) {1} finished'.format(datetime.utcnow(),
                                                      icao,n+1,total))
            logger.info(' ({1}/{2}) {0} finished'.format(icao,n+1,total))
        else:
            print('{0}: ({2}/{3}) {1} missing'.format(datetime.utcnow(),
                                                      icao,n+1,total))
            logger.info(' ({1}/{2}) {0} missing'.format(icao,n+1,total))
        time.sleep(1)
    return rpts


if __name__ == '__main__':
    icao, kind = sys.argv[1], sys.argv[2]
    print(get_rpt_from_awc(icao,kind))
