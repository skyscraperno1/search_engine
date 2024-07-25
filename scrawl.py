import requests
from scrapy import Selector
import pandas as pd
from utils import process_content

headers = {
    # 'Referer':'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=VOLT%E5%B8%81&fenlei=256&oq=VOLT%25E5%25B8%2581&rsv_pq=8298b80c003542cc&rsv_t=20b5bYc%2BB46E%2BHATf82ROZbBCS2EyrHxal4mUfBB%2FDWROjQNpB5%2FQs0qwQ4&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_btype=t&inputT=3634&rsv_n=2&rsv_sug3=7&rsv_sug1=3&rsv_sug7=100&rsv_sug2=0&rsv_sug4=3634&rsv_sug=1Sec-Ch-Ua:"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}


# pd.set_option('display.max_colwidth', 100)  # 不限制单元格最大宽度
# pd.set_option('display.width', 1000)         # 增大显示的总宽度


def get_baidu(keyword, page=1):
    if not keyword:
        raise ValueError("请输入有效内容")
    if page < 1:
        raise ValueError("页码不能小于1")
    table_headers = ["count", "link", "title", "web_name", "content"]
    data = {header: [] for header in table_headers}

    count = 0

    for i in range(page):
        current_page = i * 10
        res = requests.get(f'https://www.baidu.com/s?wd={keyword}&pn={current_page}', headers=headers)
        sel = Selector(text=res.text)
        div_list = sel.css('#content_left > div[class*="result"]:not([class*="result-op"])')
        for div in div_list:
            count = count + 1
            origin_dom = div.css('div > div:nth-child(1)')
            link = origin_dom.css('h3 > a::attr(href)').extract_first()
            title = origin_dom.css('h3 > a::text').extract_first()

            detail_dom = origin_dom.css('div:nth-child(3) > div:nth-child(1)')

            content_arr = detail_dom.css('span[class^="content-right_"] *::text').extract()
            content = ''.join(content_arr)

            website_dom = detail_dom.css('div[class*="c-row"]')
            # web_url = website_dom.css('a::attr(href)').extract_first()  # 官网地址，暂时不用
            web_name = website_dom.css('span[class="c-color-gray"]::text').extract_first()

            values = [count, link, title, web_name, content]
            for header, value in zip(table_headers, values):
                data[header].append(value)

    df = pd.DataFrame(data)
    print(df.to_string(index=False))


# get_baidu('', 2)


def get_google(keyword, page=1):
    if not keyword:
        raise ValueError("请输入有效内容")
    if page < 1:
        raise ValueError("页码不能小于1")
    table_headers = ["个数", "链接", "标题", "官网名称", "内容"]
    data = {header: [] for header in table_headers}
    count = 0
    for i in range(page):
        current_page = i * 10
        res = requests.get(f'https://www.google.com/search?q={keyword}&start={current_page}', headers=headers)
        sel = Selector(text=res.text)
        dom_list = sel.css('#search > div > div[class="dURPMd"] > div[class="MjjYud"]')
        for item in dom_list:
            count = count + 1
            title_dom = item.css('div > div > div:first-child')
            href = title_dom.css('span[jscontroller="msmzHf"] > a[jsname="UWckNb"]::attr(href)').extract_first()
            title = title_dom.css('span[jscontroller="msmzHf"] > a[jsname="UWckNb"] > h3::text').extract_first()
            website_name = title_dom.css(
                'span[jscontroller="msmzHf"] > a[jsname="UWckNb"] > div > div > div span[class="VuuXrf"]::text').extract_first()
            content_dom = item.css('div > div > div:last-child')
            content_arr = content_dom.css('div[style="-webkit-line-clamp:2"] > span *::text').extract()
            content = ''.join(content_arr)

            values = [count, href, title, website_name, content]
            for header, value in zip(table_headers, values):
                data[header].append(value)

    df = pd.DataFrame(data)
    print(df.to_string(index=False))


# get_google('', 5)


def get_bing(keyword, page=1):
    if not keyword:
        raise ValueError("请输入有效内容")
    if page < 1:
        raise ValueError("页码不能小于1")
    table_headers = ["count", "link", "title", "web_name", "content"]
    data = {header: [] for header in table_headers}
    count = 0
    for i in range(page):
        current_page = i * 10
        res = requests.get(f'https://cn.bing.com/search?q={keyword}&first={current_page}', headers=headers)
        sel = Selector(text=res.text)
        dom_list = sel.css('ol[id="b_results"] > li[class="b_algo"]')
        for item in dom_list:
            count += 1
            href = item.css('h2 > a::attr(href)').extract_first()
            title_arr = item.css('h2 > a *::text').extract()
            title = ''.join(title_arr)
            website_name = item.css('div[class="b_tpcn"] > a::attr(aria-label)').extract_first()
            content = process_content(item.css('div[class="b_caption"] > p').get())

            values = [count, href, title, website_name, content]
            for header, value in zip(table_headers, values):
                data[header].append(value)

    df = pd.DataFrame(data)
    print(df.to_string(index=False))


get_bing("", 2)
