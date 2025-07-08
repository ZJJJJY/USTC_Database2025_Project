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
    """解析标签列表页，返回基本信息+详情页URL"""
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('li.subject-item')
    books = []
    for it in items:
        try:
            title = it.select_one('a[title]')['title'].strip()
            pub = it.select_one('div.pub').get_text(strip=True).split('/')
            pub += [''] * (4 - len(pub))
            rt_tag = it.select_one('span.rating_nums')
            rating = float(rt_tag.text) if rt_tag and rt_tag.text.strip() else None
            vt_tag = it.select_one('span.pl')
            votes = int(re.search(r'(\d+)', vt_tag.text.replace(',', '')).group(1)) if vt_tag and vt_tag.text else 0
            detail_url = it.select_one('a')['href']
            books.append({
                'title': title,
                'author': pub[0].strip(),
                'publisher': pub[1].strip(),
                'pub_date': pub[2].strip(),
                'price': pub[3].strip(),
                'rating': rating,
                'votes': votes,
                'detail_url': detail_url
            })
        except Exception:
            continue
    return books

def fetch_detail(detail_url):
    """抓摘要和封面"""
    resp = session.get(detail_url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    intro = soup.find('div', id='link-report')
    img = soup.select_one('a.nbg img')
    return {
        'summary': intro.get_text(strip=True) if intro else '',
        'image_url': img['src'] if img else ''
    }

def fetch_comments(detail_url, limit=10):
    """抓取前 limit 条短评"""
    comments = []
    url = detail_url + 'comments/'
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    for span in soup.select('span.short')[:limit]:
        comments.append(span.get_text(strip=True))
    return comments

def fetch_reviews(detail_url, limit=2):
    """抓取前 limit 条长评"""
    reviews = []
    url = detail_url + 'reviews'
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = [a['href'] for a in soup.select('div.main-bd h2 a[href*="/review/"]')[:limit]]
    for link in links:
        t = session.get(link, timeout=30)
        t.raise_for_status()
        detail_soup = BeautifulSoup(t.text, 'html.parser')
        content = detail_soup.select_one('div.review-content')
        if content:
            reviews.append(content.get_text(strip=True))
        time.sleep(random.uniform(1,2))
    return reviews

def crawl_tag(tag, pages=5):
    all_data = []
    for p in range(pages):
        html = fetch_tag_page(tag, p)
        basic_list = parse_list(html)
        for b in basic_list:
            # 1. 基本信息 + 摘要 + 图片
            detail = {}
            try:
                detail = fetch_detail(b['detail_url'])
            except:
                pass
            # 合并字典
            b.update(detail)
            # 2. 短评
            try:
                b['comments'] = fetch_comments(b['detail_url'], limit=10)
            except:
                b['comments'] = []
            # 3. 长评
            try:
                b['reviews'] = fetch_reviews(b['detail_url'], limit=2)
            except:
                b['reviews'] = []
            all_data.append(b)
            time.sleep(random.uniform(1,2))
        time.sleep(random.uniform(2,4))
    return all_data

def save_csv(data, tag):
    if not data:
        print(f'⚠️ tag="{tag}" 无数据，跳过')
        return
    # 展开 comments/reviews 成多行
    rows = []
    for book in data:
        for c in book.get('comments', []):
            rows.append({'标签': tag, '标题': book['title'], '作者': book['author'],
                         '类型': '短评', '内容': c})
        for r in book.get('reviews', []):
            rows.append({'标签': tag, '标题': book['title'], '作者': book['author'],
                         '类型': '长评', '内容': r})
    df = pd.DataFrame(rows)
    filename = f'douban_{tag}_with_comments.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'✅ 已保存 {len(df)} 条到 {filename}')

# ------------- 主程序 -------------
if __name__ == '__main__':

    tags = ['文学']

    for tag in tags:
        print(f'▶️ 爬取标签：{tag}')
        data = crawl_tag(tag, pages=5)
        save_csv(data, tag)
