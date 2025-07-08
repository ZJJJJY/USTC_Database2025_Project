import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ------------- 配置区 -------------
COOKIES = {
    'bid': 'gRV82B3zAbk',
    'ck': 'u2Y5',
    'dbcl2': '"265584954:y73u5oh0/8A"',
}
USE_PROXY = os.environ.get('USE_PROXY', '0') == '1'
PROXIES = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    ),
    'Referer': 'https://book.douban.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

def create_session():
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)
    if USE_PROXY:
        session.proxies.update(PROXIES)
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[403,500,502,503,504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

session = create_session()

# ------------- 功能函数 -------------

def fetch_tag_page(tag, page):
    url = f'https://book.douban.com/tag/{tag}?start={page*20}&type=T'
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text

def parse_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('li.subject-item')
    books = []
    for it in items:
        try:
            title = it.select_one('a[title]')['title'].strip()
            pub = it.select_one('div.pub').get_text(strip=True).split('/')
            pub += [''] * (4 - len(pub))

            # 评分
            rt_tag = it.select_one('span.rating_nums')
            rating = float(rt_tag.text) if rt_tag and rt_tag.text.strip() else None

            # 评论人数
            vt_tag = it.select_one('span.pl')
            votes = int(re.search(r'(\d+)', vt_tag.text.replace(',', '')).group(1)) if vt_tag and vt_tag.text else 0

            detail_url = it.select_one('a')['href']

            books.append({
                'title':     title,
                'author':    pub[0].strip(),
                'publisher': pub[1].strip(),
                'pub_date':  pub[2].strip(),
                'price':     pub[3].strip(),
                'rating':    rating,
                'votes':     votes,
                'detail_url': detail_url
            })
        except Exception:
            # 跳过解析失败的条目
            continue
    return books

def fetch_detail(detail_url):
    resp = session.get(detail_url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    intro = soup.find('div', id='link-report')
    img_tag = soup.select_one('a.nbg img')
    return {
        'summary':   intro.get_text(strip=True) if intro else '',
        'image_url': img_tag['src'] if img_tag else ''
    }

def crawl_tag(tag, pages=5):
    all_books = []
    for p in range(pages):
        try:
            html = fetch_tag_page(tag, p)
            basic_list = parse_list(html)
        except Exception as e:
            print(f'[列表页失败] tag={tag} page={p+1}: {e}')
            basic_list = []

        for b in basic_list:
            time.sleep(random.uniform(1, 2))
            try:
                detail = fetch_detail(b['detail_url'])
            except Exception:
                detail = {'summary': '', 'image_url': ''}
            b.update(detail)
            all_books.append(b)

        time.sleep(random.uniform(2, 4))
    return all_books

def save_csv(data, tag):
    if not data:
        print(f'⚠️ tag="{tag}" 无数据，跳过保存')
        return
    df = pd.DataFrame(data)
    # 删除 detail_url 列
    df = df.drop(columns=['detail_url'])
    # 重命名列为中文
    df = df.rename(columns={
        'title': '标题',
        'author': '作者',
        'publisher': '出版社',
        'pub_date': '出版日期',
        'price': '价格',
        'rating': '评分',
        'votes': '评论人数',
        'summary': '摘要',
        'image_url': '图片链接'
    })
    filename = f'douban_{tag}.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'✅ 已保存 {len(df)} 条到 {filename}')

# ------------- 主程序 -------------
if __name__ == '__main__':
    with open('tags_2.txt', 'r', encoding='utf-8') as f:
        tags = [line.strip() for line in f if line.strip()]
        
    for tag in tags:
        print(f'▶️ 开始爬取标签: {tag}')
        results = crawl_tag(tag, pages=5)
        save_csv(results, tag)
