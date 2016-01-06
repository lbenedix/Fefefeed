import dataset
import time
from email import utils
from bs4 import BeautifulSoup

feed = '<rss version="2.0">\n<channel>\n<title>Fefes Blog</title>\n<link>http://blog.fefe.de/</link>\n<description>Verschwörungen und Obskures aus aller Welt</description>\n<language>de</language>\n\n'

db = dataset.connect('sqlite:///fefe.db')
all_items = [x for x in db['items'].find(order_by='-timestamp')]


for item in all_items[:50]:
    feed += '<item>\n'
    feed += '<link>http://blog.fefe.de/?ts={}</link>\n'.format(item['item_id'])
    feed += '<guid>http://blog.fefe.de/?ts={}</guid>\n'.format(item['item_id'])
    feed += '<pubDate>{}</pubDate>\n'.format(utils.formatdate(time.mktime(item['timestamp'].timetuple())))

    words = BeautifulSoup(item['text'], 'html5lib').text.split(' ')
    feed += '<title>{}'.format(' '.join(words[:10]))
    if len(words) > 10: feed += '...</title>\n'
    else:               feed += '</title>\n'
    feed += '<description>\n<![CDATA[\n{}\n]]>\n</description>\n'.format(item['text'])
    feed += '</item>\n'

feed += '</channel>\n</rss>'


text_file = open("feed.xml", "w")
text_file.write(feed)
text_file.close()
