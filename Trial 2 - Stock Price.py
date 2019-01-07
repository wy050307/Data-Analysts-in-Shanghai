from requests_html import HTMLSession
session = HTMLSession()

links = ['http://stock.finance.sina.com.cn/usstock/quotes/aapl.html',
         'http://stock.finance.sina.com.cn/usstock/quotes/bidu.html',
         'http://stock.finance.sina.com.cn/usstock/quotes/msft.html']

for link in links:
    r = session.get(link)
    r.html.render()
    price = r.html.find('#hqPrice', first=True)
   # stock = r.html.find('body > div:nth-child(7) > div.R > div.sec.clearfix > div.l > div.block.block_hq > div.name > h1 > span', first=True)
    print(price.text)
