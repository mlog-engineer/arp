# coding: utf-8
import json as js
import os
from collecter import get_rpt_from_awc
import time

if not os.path.exists('./airports.json'):
    print('can\'t find ispt_list.json file')
    exit()
else:
    with open('./airports.json') as f:
        airports = js.load(f)

def main():
    result = {'valid':[],'invalid':[]}
    for ap in airports:
        rpt = get_rpt_from_awc(ap,'metar')
        print('inspecting {}'.format(ap))
        if rpt:
            result['valid'].append(ap)
            print('valid')
        else:
            print('invalid')
            result['invalid'].append(ap)
        time.sleep(2)

    with open('./ispt_result.json','w') as f:
        js.dump(result,f)

if __name__ == '__main__':
    main()
