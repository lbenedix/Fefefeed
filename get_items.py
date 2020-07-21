import requests, dataset
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib

def dates():
    now = datetime.now()
    for y in range(2005,now.year + 1):
        for m in range(1,13):
            yield '{}{:02d}'.format(y,m)

url = 'http://blog.fefe.de/?mon={}'

db = dataset.connect('sqlite:///fefe.db')
table = db['items']

now = datetime.now()

dates = sorted(dates())

index = dates.index('{}{:02d}'.format(now.year,now.month))

for i in range(2):
    d = dates[index-i]
#for d in dates:
#    print(datetime.now(), d)
    y = int(d[:4])
    m = int(d[4:])

    print(datetime.now(), url.format(d))
    soup = BeautifulSoup(requests.get(url.format(d)).text, 'html5lib')

    c = 0
    for li in soup.find_all('li'):
        if li.text[:3] != '[l]': continue

        id = li.find_all('a')[0].attrs['href'][4:]
        ts = datetime.fromtimestamp(int(id, 16) ^ 0xfefec0de)

        text = ''.join(map(str, li.contents[1:]))

        updated = False
        update_ts = None
        if table.count(item_id=id) > 0:
            old_item = table.find_one(item_id=id)
            old_text = old_item['text']
            update_ts = old_item['update_ts']
            if old_text != text:
                print(datetime.now(), 'updated', id)
                ts = datetime.now()
                updated = True
                db['updates'].insert(dict(item_id=id, timestamp=ts))
        #else:
        #    print(datetime.now(), 'new    ', id)

        if updated:
            update_ts = datetime.now()

        table.upsert(dict(item_id=id,timestamp=ts,text=text, update_ts=update_ts),['item_id'])
        c += 1
