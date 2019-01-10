# Ref : https://python123.io/tutorials/web_crawler/index.html#/

#from requests_html import HTMLSession
#session = HTMLSession()
#r = session.get('https://movie.douban.com/subject/1292052/')
#title = r.html.find('#link-report > span.short > span', first=True)
# r.html.find() 接受一个 CSS 选择器（字符串形式）作为参数
# 返回在网页中使用该选择器选中的内容
#print(title.text)


from requests_html import HTMLSession
import csv

session = HTMLSession()

file = open('Trial 1 - Douban.csv', 'w', newline='')
csvwriter = csv.writer(file)
csvwriter.writerow(['名称', '年份'])

links = ['https://movie.douban.com/subject/1292052/',
         'https://movie.douban.com/subject/26752088/',
         'https://movie.douban.com/subject/1962665/']

for link in links:
    r = session.get(link)
    title = r.html.find('#content > h1 > span:nth-child(1)', first=True)
    year = r.html.find('#content > h1 > span.year', first=True)
    csvwriter.writerow([title.text, year.text])

file.close()