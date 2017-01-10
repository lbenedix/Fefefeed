import dataset
import time
from datetime import datetime
from email import utils
from bs4 import BeautifulSoup
from xml.sax.saxutils import escape

feed = '<rss version="2.0"><channel><title>Fefes Blog</title><link>http://blog.fefe.de/</link><description>Verschwörungen und Obskures aus aller Welt</description><language>de</language>'

feed += '<lastBuildDate>{}</lastBuildDate>'.format(utils.formatdate(time.mktime(datetime.now().timetuple())))


db = dataset.connect('sqlite:///fefe.db')
all_items = [x for x in db['items'].find(order_by='-timestamp')]


for item in all_items[:50]:
    feed += '<item>'
    feed += '<link>http://blog.fefe.de/?ts={}</link>'.format(item['item_id'])
    feed += '<guid>http://blog.fefe.de/?ts={}'.format(item['item_id']) 
    if item['update_ts'] != None:
        feed += '#{}'.format(item['update_ts'])
    feed += '</guid>'
    feed += '<pubDate>{}</pubDate>'.format(utils.formatdate(time.mktime(item['timestamp'].timetuple())))

    words = BeautifulSoup(item['text'], 'html5lib').text.split(' ')
    feed += '<title>{}'.format(escape(' '.join(words[:10])))
    if len(words) > 10: feed += '...</title>\n'
    else:               feed += '</title>\n'
    feed += '<description><![CDATA[{}]]></description>'.format(item['text'])
    feed += '</item>'

feed += '</channel></rss>'

text_file = open("feed.xml", "w")
text_file.write(feed)
text_file.close()
