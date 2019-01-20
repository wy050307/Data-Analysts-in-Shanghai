from requests_html import HTMLSession
import re
import csv
# from matplotlib import pyplot as plt

'''
Web Crawl
'''

# 设置所要提取的元素
# --1 工资
salary_element = '<p.*>(\d+)K-(\d+)K</p>'
salary = []

# --2 公司名称
company_element = '<a.* company_title">(.*)</a>'
company = []
# HTML:<a href="https://company.zhaopin.com/CZ138117190.htm" title="北京外企德科人力资源服务上海有限公司"
# target="_blank" class="contentpile__content__wrapper__item__info__box__cname__title company_title"
# >北京外企德科人力资源服务上海有限公司</a>

# --3 职位名称
job_element = '<span title="(.*)" class=.*</span>'
job = []
# HTML: <span title="初级数据分析师" class="contentpile__content__wrapper__item__info__box__jobname__title"
# >初级<span style="color: #FF5959;">数据分析师</span></span>

# 设置停止符
disabled_button_element = '<button.* disabled="disabled".*disable">下一页</button>'
#disabled_button_element = '<button disabled="disabled" class="btn soupager__btn soupager__btn--disable">下一页</button>'
# CSS: pagination_content > div > button.btn.soupager__btn.soupager__btn--disable
# HTML: <button disabled="disabled" class="btn soupager__btn soupager__btn--disable">下一页</button>

disabled_button = None
p = 1

"""
## test disabled_button effectiveness
# url = 'https://sou.zhaopin.com/?p=3&jl=538&in=10900&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88&kt=3'
# session = HTMLSession()
# page = session.get(url)
# page.html.render(sleep=3)
# disabled_button = re.findall(disabled_button_element, page.html.html)
# print(disabled_button)
"""

while not disabled_button:
    print('\n正在爬取第' + str(p) + '页')
    url = 'https://sou.zhaopin.com/?p=' + str(p) + '&jl=538&in=10900&kw=数据分析师&kt=3'
    # https://sou.zhaopin.com/?p=2&jl=538&kw=数据分析师&kt=3

    session = HTMLSession()
    page = session.get(url)
    page.html.render(sleep=3) #用于读取动态内容

    # 提取出薪资，保存为形如 [[10,20], [15,20], [12, 15]] 的数组
    salary += re.findall(salary_element, page.html.html)
    # set the salaries into a variable
    temp = re.findall(salary_element, page.html.html)
    print(temp)

    # 提取出公司名，并保存为['彪洋科技(北京)有限公司', '上海晶樵网络信息...]
    company += re.findall(company_element, page.html.html)
    temp2 = re.findall(company_element, page.html.html)
    print(temp2)

    # 提取职位名称
    job += re.findall(job_element, page.html.html)
    temp3 = re.findall(job_element, page.html.html)
    print(temp3)

    # 判断页面中下一页按钮还能不能点击
    disabled_button = re.findall(disabled_button_element, page.html.html)

    p = p + 1
    session.close()

'''
写入 csv
'''
print('\nSaving into csv ...')

# 新建 csv
file = open('Trial 3 - Salaries.csv', 'w', newline='')
csvwriter = csv.writer(file)
csvwriter.writerow(['Company', 'Job_Title', 'Salary_Low', 'Salary_High', 'Salary Type'])
# 写入 csv
salary_type = []
i = 0
for s in salary:
    # 提取公司名字
    company_name = company[i]
    job_title = job[i]
    salary_low = s[0]
    salary_high = s[1]

    # 求出每家公司的平均薪资，比如 [12, 15] 的平均值为 13
    salary_mean = (int(s[0]) + int(s[1])) / 2
    # 划定薪资范围
    if salary_mean <= 15:
        salary_type = 'Low Salary'
    elif (salary_mean > 15) and (salary_mean <= 30):
        salary_type = 'middle_salary'
    else:
        salary_type = 'middle_salary'
    # 写入 csv
    csvwriter.writerow([company_name, job_title, salary_low, salary_high, salary_type])
    i += 1

"""
Ref: Python123 （2019-01-11）

# 作图
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
"""



