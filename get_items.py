import requests, dataset
from bs4 import BeautifulSoup
from datetime import datetime

def dates():
    for y in range(2005,2017):
        for m in range(1,13):
            yield '{}{:02d}'.format(y,m)

url = 'http://blog.fefe.de/?mon={}'

db = dataset.connect('sqlite:///fefe.db')
table = db['items']

now = datetime.now()

dates = sorted(dates())

index = dates.index('{}{:02d}'.format(now.year,now.month))

# for i in range(3):
#     d = dates[index-i]
for d in dates:
    y = int(d[:4])
    m = int(d[4:])

    soup = BeautifulSoup(requests.get(url.format(d)).text, 'html5lib')

    c = 0
    for li in soup.find_all('li'):
        if li.text[:3] != '[l]': continue

        id = li.find_all('a')[0].attrs['href'][4:]
        ts = datetime.fromtimestamp(int(id, 16) ^ 0xfefec0de)

        text = ''.join(map(str, li.contents[1:]))

        if table.count(item_id=id) > 0:
            old_text = table.find_one(item_id=id)['text']
            if old_text != text:
                print(datetime.now(), 'updated', id)
        # else:
        #     print(datetime.now(), 'new    ', id)

        table.upsert(dict(item_id=id,timestamp=ts,text=text),['item_id'])
        c += 1
    print(datetime.now(), d, c)

