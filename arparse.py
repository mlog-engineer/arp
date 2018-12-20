# coding: utf-8
'''航空天气报文解析程序

本程序可以解析处理的报文包括：
    1、例行天气报告（METAR）
    2、特选天气报告（SPECI）
    3、机场天气报告（TAF）
'''
import re
import os

field_patterns = {
    # 报文类型
    'kind':             r'(METAR|SPECI|TAF)',
    # 发报时间
    'time':             r'\d{6}Z',
    # 机场编码
    'cccc':             r'\b[A-Z]{4}\b',
    # 风向风速（风速变化）
    'wind':             r'(\d{3}|VRB)\d{2}[G\d{2}]*(MPS|KT)'\
                            '( \d{3}V\d{3})?',
    # 温度/露点温度
    'temp':             r'\bM?\d{2}/M?\d{2}\b',
    # 修正海平面气压
    'QNH':              r'Q\d{4}',
    # 自动观测标识
    'auto':             r'AUTO',
    # 修正报标识
    'correct':          r'COR',
    # 好天气
    'cavok':            r'CAVOK',
    # 跑道视程
    'rvr':              r'R\d{2}[RLC]?/(\d{4}V)?[PM]?'\
                            '\d{4}[UDN]?',
    # 垂直能见度
    'vvis':                r'VV\d{3}',
    # 能见度
    'vis':              r'(?<=\s)\d{4}[A-Z]*\b',
    # 云量云高
    'cloud':            r'(FEW|SCT|BKN|OVC|SKC|NSC)'\
                            '(\d{3})?([A-Za-z]*)?',
    # 天气现象
    'weather':          r'(?<=\s)(?:\+|-|VC)?'\
                            '(MI|BC|PR|DR|BL|SH|TS|FZ)?'\
                            '(DZ|RA|SN|SG|IC|PL|GR|GS)?'\
                            '(BR|FG|FU|VA|DU|SA|HZ)?'\
                            '(PO|SQ|FC|SS|DS)?(?=\s)',
    # 风切变
    'wshear':           r'WS (LDG |TKOF |ALL )?RWY\d+[LRC]?',
    # 趋势
    'trend':            r'(TEMPO|BECMG|NOSIG).*?(?= TEMPO| BECMG| NOSIG|=)',
    # 变化起止时间
    'vartime':          r'(FM|TL|AT)\d{4}',
    # 当前观测
    'observation':      r'(METAR|SPECI|TAF).+?(?= TEMPO| BECMG| NOSIG)',
    # 预报有效时间
    'validtime':        r'\b\d{6}\b',
    # 预报取消标识
    'cancel':           r'CNL',
    # 修复预报标识
    'amend':            r'AMD',
    # 预报温度
    'txtn':             r'TXM?\d+/M?\d+Z\sTNM?\d+/M?\d+Z'
}

def abstract_field(field, text, mod='first'):
    '''提取文本字段

    输入参数
    -------
    field : `str`
        报文字段名称，选项如下(中括号内的字段不一定会出现)：
            'observation'  非趋势全部字段
            'kind'         报文种类
            'cccc'         机场ICAO码
            'time'         发报时间
            'wind'         风向风速 [风速变化]
            'temp'         温度/露点温度
            'QNH'          修正海平面气压
            'trend'        变化趋势
            'cavok'        [好天气标识]
            'auto'         [自动观测标识]
            'correct'      [修正报标识]
            'rvr'          [跑道视程]
            'vvis'         [垂直能见度]
            'vis'          [能见度]
            'cloud'        [云量云高[云形]]
            'weather'      [天气现象]
            'wshear'       [跑道风切变]
            'vartime'      [趋势变化起止时间]
            'validtime'    预报有效时间
            'cancel'       [预报取消标识]
            'amend'        [预报修正标识]
            'nsw'          [重要天气现象结束标识]
            'prob'         [概率预报组]
            'txtn'         预报气温组

    text : `str`
        所要查找的原始报文字符串

    mod : `str`
        匹配模式，可供选择的选项有'first'和'all'。
            'first'表示匹配第一个，'all'表示匹配所有，默认为'first'。

    返回值
    -----
    `str` | `list` | None :
        从原始报文中提取出的相应字段，若mod为'first'则结果返回字符串`str`；
            若mod为'all'，则返回列表`list`；
            若原始报文中无相应字段则返回None

    示例
    ----
    >>> text = 'METAR ZSNJ 030500Z 24002MPS 330V030 1000 '\
               'R06/1300U R07/1300N BR FEW005 15/14 Q1017 NOSIG='
    >>> abstract_field('wind',text)
    '24002MPS 330V030'

    >>> abstract_field('rvr',text)
    'R06/1300U'
    '''
    if mod == 'first':
        match = re.search(field_patterns[field],text)
        if match:
            return match.group()
        else:
            return None
    elif mod == 'all':
        iter = re.finditer(field_patterns[field],text)
        matchs = []
        while True:
            try:
                match = next(iter)
            except StopIteration:
                break
            else:
                matchs.append(match.group())
        if matchs:
            return matchs
        else:
            return None


if __name__ == '__main__':

    text = 'TAF AMD ZHHH 192112Z 192106 04003MPS 1200 '\
            'BR NSC TX15/06Z TN08/21Z BECMG 2223 0700 FG'\
            ' BECMG 0102 1600 BR BECMG 0304 3000 BR='

    abstract_field('cavok',text,mod='all')
