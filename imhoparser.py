#!/usr/bin/python3
# * coding: utf8 *
from lxml.html import document_fromstring
import urllib
import urllib.request
import simplejson

import sys


if len(sys.argv) < 2:
    print('USAGE: imhoparser.py username')
    quit()


def get_attr(element, xpath, name):
    found = element.xpath(xpath)
    if found is None or len(found) <= 0:
        return ''
    return found[0].get(name)


username = sys.argv[1]
firstPart = True
print('{')
for content in ['films', 'books']:

    if firstPart:
        firstPart = False
    else:
        print(',')

    print('"%s" : [' % content)
    first = True
    for rate in range(1, 11):

        url = 'http://%s.imhonet.ru/content/%s/rates/%d' % (username, content, rate)
        while 1:

            opener = urllib.request.build_opener()
            # opener.addheaders.append(('Cookie', ''))
            opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'))
            text = opener.open(url).read()
            doc = document_fromstring(text)

            for element in doc.xpath('//*[contains(@class, "m-inlineitemslist-item")]'):

                item = {
                    'content': {},
                    'rate': rate,
                    'imhonet': {
                        'object-id': element.get('data-object_id'),
                        'cover': get_attr(element, '*[contains(@class, "m-inlineitemslist-image")]', 'data-original')
                    }
                }

                linkElement = element.xpath('.//*[@class="m-inlineitemslist-describe-h2"]/a')[0]
                item['content']['link'] = linkElement.get('href')
                item['content']['title'] = linkElement.text.strip()

                country = element.xpath('.//*[@class="m-inlineitemslist-describe-gray"]')[0].text.strip()
                if country != '':
                    item['content']['country'] = country

                if first:
                    first = False
                else:
                    print(',')

                print(simplejson.dumps(item, ensure_ascii=False))

            pagination = doc.xpath('//*[@class = "m-pagination"]/a')
            if len(pagination) and pagination[len(pagination) - 1].find('span').get('data-content') == u'\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0430\u044f &rightarrow;':
                url = pagination[len(pagination) - 1].get('href')
            else:
                break
    print(']')
print('}')

