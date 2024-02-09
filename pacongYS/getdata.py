# -*- coding: utf-8 -*-

"""
爬取任务内容:
1.文章URL
2.标题
3.内容
4.标题图片
5.时间
"""
from bs4 import BeautifulSoup     # 网页解析，获取数据
import re       # 正则表达式，进行文字匹配
import urllib.request
import urllib.error  # 制定URL，获取网页数据,报错处理
from datetime import datetime
import db_control       # 自定义msyql库包


targetURL = 'https://news.cctv.com/yskp/index.shtml?spm=C96370.PPDB2vhvSivD.EpexGtoFhhxD.4'       # 目标URL
re_UrlLink = re.compile(r'"url": "([^"]+)"')        # 匹配html中的所有url内容
re_title = re.compile(r'"title": "([^"]+)"')        # 匹配html中所有的title内容
re_img = re.compile(r'"imgUrl": "([^"]+)"')         # 匹配html中所有的img内容
re_date = re.compile(r'"date": "([^"]+)"')          # 匹配html中所有的date内容


# 处理目标URL的
def get_data(targetURL):
    i = 0
    dataList = []
    date_format = "%Y年%m月%d日"
    html_content =request_url(targetURL)

    if (len(html_content) == 0):
        print("没有爬取到内容")
    else:
        # 对接受到的html_content进行处理,找到所有的url、title、content、imgurl(标题图)、date
        urls = re.findall(re_UrlLink, html_content)

        titles = re.findall(re_title, html_content)

        contens = get_single_content(urls)

        img_urls = re.findall(re_img, html_content)
        img_urls_with_https = ['https:' + url for url in img_urls]      # 添加https:,用于访问图片

        dates = re.findall(re_date, html_content)
        standard_time = [datetime.strptime(date_str, date_format) for date_str in dates]        # 转化成标准时间

        dataList = merge_individual_data(urls, titles, contens, img_urls_with_https, standard_time)
    return dataList


# 融合单个整体数据（文章URL、标题、内容、标题图片、时间）
def merge_individual_data(urls, titles, contens, img_urls_with_https, standard_time):
    datalist = []
    length = len(urls)      # 大概300条
    i = 0

    for i in range(0, length):
        data = []       # 一次循环一个列表存储数据
        data.append(str(i+1))       # 用于主键记录
        data.append(urls[i])
        data.append(titles[i])
        data.append(contens[i])
        data.append(img_urls_with_https[i])
        data.append(standard_time[i])
        datalist.append(data)

        # print(data)
        # break
    return datalist

# 获取每个文章url里的内容


def get_single_content(urls):
    contents = []
    html_content = ""
    for url in urls:
        html_content = request_url(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        # 提取所有 <p> 标签的文本内容
        p_contents = [p.get_text(strip=True)for p in soup.find_all('p')]

        # 去除最后两个p标签的内容：'央视评论员', '扫二维码 访问央视网'
        p_contents = p_contents[:-2]

        p_contents = [content for content in p_contents if content]     # 去除空元素

        p_contents = [f'<p>{content}</p>' for content in p_contents if content]  # 在每个元素前后添加<p></p>

        p_contents = "".join(p_contents)        # 拼接成字符串
        
        contents.append(p_contents)

        # print(p_contents)
        # break
    return contents


# 访问目标URL,获取html内容
def request_url(url):
    html = ""
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html_content = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if (hasattr(e, "code")):
            print(e.code)
        if (hasattr(e, "reason")):
            print(e.reason)
    return html_content



def main():
        # 获取所有文章的信息
        datalist = get_data(targetURL)
        # 连接数据库
        connection = db_control.create_connection()

        # 插入数据
        res = db_control.insert_article(connection,datalist)
        return res

if __name__ == '__main__':
    res = main()
    if(res):
        print(f"爬取完毕,已经将数据放置{db_control.database_name}数据库的{db_control.table_name}表中!")
