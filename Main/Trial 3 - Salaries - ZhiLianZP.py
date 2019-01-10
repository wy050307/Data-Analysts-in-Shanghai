from requests_html import HTMLSession
import re
from matplotlib import pyplot as plt

salary_element = '<p.*>(\d+)K-(\d+)K</p>'
salary = []
disabled_button_element = '<button disabled="disabled" class="btn soupager__btn soupager__btn--disable">下一页</button>'
# CSS: pagination_content > div > button.btn.soupager__btn.soupager__btn--disable
# HTML: <button disabled="disabled" class="btn soupager__btn soupager__btn--disable">下一页</button>

disabled_button = None
p = 1

## test disabled_button effectiveness
# url = 'https://sou.zhaopin.com/?p=3&jl=538&in=10900&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88&kt=3'
# session = HTMLSession()
# page = session.get(url)
# page.html.render(sleep=3)
# disabled_button = re.findall(disabled_button_element, page.html.html)
# print(disabled_button)

while not disabled_button:
    print('正在爬取第' + str(p) + '页')
    url = 'https://sou.zhaopin.com/?p=' + str(p) + '&jl=538&in=10900&kw=数据分析师&kt=3'
    # https://sou.zhaopin.com/?p=2&jl=538&kw=数据分析师&kt=3

    session = HTMLSession()
    page = session.get(url)
    page.html.render(sleep=3)
    # 提取出薪资，保存为形如 [[10,20], [15,20], [12, 15]] 的数组
    salary += re.findall(salary_element, page.html.html)
    temp = re.findall(salary_element, page.html.html)
    print(temp)
    # 判断页面中下一页按钮还能不能点击
    disabled_button = re.findall(disabled_button_element, page.html.html)
    p = p + 1
    session.close()

# 求出每家公司的平均薪资，比如 [12, 15] 的平均值为 13
salary = [(int(s[0]) + int(s[1])) / 2 for s in salary]
# 划定薪资范围，便于展示，你也可以尝试其它展示方案
low_salary, middle_salary, high_salary = [0, 0, 0]
for s in salary:
    if s <= 15:
        low_salary += 1
    elif s > 15 and s <= 30:
        middle_salary += 1
    else:
        high_salary += 1
# 调节图形大小，宽，高
plt.figure(figsize=(6, 9))
# 定义饼状图的标签，标签是列表
labels = [u'<15K', u'15K-30K', u'>30K']
data = [low_salary, middle_salary, high_salary]
plt.pie(data, labels=labels)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
plt.legend()
plt.show()



