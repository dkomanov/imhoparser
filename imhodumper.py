#!/usr/bin/python3
# * coding: utf8 *

import urllib
import urllib.request
import json
import sys
import time


if len(sys.argv) < 2:
    print('USAGE: imhodumper.py username')
    quit()


username = sys.argv[1]
page = 1
mySecretCookie = ''
result = {
    "movies": []
}


def getUrl(p):
    return 'http://{0}.imhonet.ru/web.php?path=content/films/rates/&domain=user&user_domain={0}&page={1}'.format(username, p)

def debug(msg):
    sys.stderr.write('{}\n'.format(msg))


while (True):
    url = getUrl(page)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('Cookie', mySecretCookie),
        ('Accept', 'application/json'),
        ('Referer', 'http://{}.imhonet.ru/content/films/rates/'.format(username)),
        ('X-Requested-With', 'XMLHttpRequest'),
        ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.85 Chrome/45.0.2454.85 Safari/537.36')
    ]

    try:
        r = opener.open(url)
    except Exception as detail:
        debug('got exception @ {}: {}'.format(page, detail))
        break

    allJson = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    user_rates = allJson["user_rates"]
    content_rated = user_rates["content_rated"]

    result["movies"].extend(content_rated)

    debug('page {}, movies {}'.format(page, len(content_rated)))

    if len(content_rated) <= 0:
        break
    else:
        page += 1

    #time.sleep(1)


debug('total movies {}'.format(len(result["movies"])))
print(json.dumps(result, ensure_ascii=False, indent='  '))

