import requests as r
import urllib
import html
import argparse
from datetime import datetime as d

api_key = open('api.key', 'r').read()
output_type = 'ADIF'
url = 'https://logbook.qrz.com/api'

def get_qso(call):
    post_data = {
        'KEY' : api_key,
        'ACTION' : 'fetch',
        'OPTION' : 'CALL:'+call+','+'TYPE:'+output_type
    }

    post_data = urllib.parse.urlencode(post_data)

    resp = r.post(url, data=post_data)
    str_resp = resp.content.decode('utf-8')
    html_resp = urllib.parse.unquote(str_resp)
    response = html.unescape(html_resp)

    pre_adif = response.split('&')

    for param in pre_adif:
        if 'ADIF=' in param:
            raw_adif = param[5:len(param)]
            adif = raw_adif.strip()
        else:
            pass

    return adif

def qsl_sent(call):
    now = d.now()
    now = now.strftime('%Y%m%d')

    in_date = input('Sent [{}]: '.format(now))

    if in_date == '':
        in_date = now

    adif = get_qso(call)
    new_adif = adif.replace('<qsl_sent:1>N', '<qsl_sent:1>Y\n<qslsdate:8>{}'.format(in_date))

    print(new_adif)

    confirm_update = input('Update record? [y/N] ')
    if confirm_update == 'y':
        print('Updating record...')
        return update_qso(new_adif)
    else:
        return 'Record not updated.'

def qsl_rcvd(call):
    now = d.now()
    now = now.strftime('%Y%m%d')

    in_date = input('Sent [{}]: '.format(now))

    if in_date == '':
        in_date = now

    adif = get_qso(call)
    new_adif = adif.replace('<qsl_rcvd:1>N', '<qsl_rcvd:1>Y\n<qslrdate:8>{}'.format(in_date))

    confirm_update = input('Update record? [y/N] ')
    if confirm_update == 'y':
        print('Updating record...')
        return update_qso(new_adif)
    else:
        return 'Record not updated.'

def update_qso(new_adif):
    print(new_adif)

    post_data = {
        'KEY' : api_key,
        'ACTION' : 'insert',
        'OPTION' : 'replace',
        'ADIF' : new_adif
    }

    post_data = urllib.parse.urlencode(post_data)

    print(post_data)

    resp = r.post(url, data=post_data)

    str_resp = resp.content.decode('utf-8')
    html_resp = urllib.parse.unquote(str_resp)
    response = html.unescape(html_resp)

    return response


parser = argparse.ArgumentParser()
parser.add_argument('action', type=str)
parser.add_argument('call', type=str)
args = parser.parse_args()

action = args.action
call = args.call

if action == 'get':
    print(get_qso(call))
if action == 'rcvd':
    print(qsl_rcvd(call))
if action == 'sent':
    print(qsl_sent(call))