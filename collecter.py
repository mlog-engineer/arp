# coding: utf-8
import urllib.request
import urllib.parse
import random

def get_rpt_from_awc(icao,buffer,kind='metar'):
    '''按机场ICAO码获取报文，数据来自 AWC: https://aviationweather.gov/

    输入参数
    -------
    icao : `str`
        所要查询的机场ICAO码，如'ZBAA'、'ZUUU'
    buffer : `str`
        暂存目录路径，程序将把目标网页下载到该目录下，再读取解析
        注意，路径末尾须带有斜杠，例如 : '/home/buffer/'
    kind : `str`
        报文类型，须在'metar'和'taf'中选择，默认为'metar'

    返回值
    -----
    `str` : 目标机场最新的航空报文

    示例
    ---
    >>> from collecter import get_rpt_from_awc
    >>> get_rpt_from_awc('ZBAA','./','metar')
    'METAR ZBAA 030400Z 03005MPS 340V070 CAVOK 07/M21 Q1026 NOSIG'
    '''
    def random_header():
        header_list = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
              ]
        return random.choice(header_list)

    def get_url(icao,kind):
        if kind == 'metar':
            return 'https://aviationweather.gov/metar/data?ids='+icao
        elif kind == 'taf':
            return 'https://aviationweather.gov/taf/data?ids='+icao

    def save_web(req,savepfn):
        web_code = urllib.request.urlopen(req).read()
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
    save_web(req,buffer+'web.html')
    rpt = parse_rpt(buffer+'web.html',kind)
    if rpt and kind == 'metar':
        rpt = ' '.join([kind.upper(),rpt])
    return rpt

if __name__ == '__main__':
    get_rpt_from_awc('ZBAA',kind='metar')
