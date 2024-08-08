from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import logging


class NankaiNewsScraper:
    def __init__(self, driver_path, url):
        self.driver_path = driver_path
        self.url = url

    def fetch_dynamic_webpage_content(self, url):
        try:
            edge_options = Options()
            edge_options.add_argument("--headless")
            edge_options.add_argument("--disable-gpu")
            service = EdgeService(executable_path=self.driver_path)
            driver = webdriver.Edge(service=service, options=edge_options)
            driver.get(url)
            driver.implicitly_wait(10)
            page_source = driver.page_source
            driver.quit()
            return page_source
        except Exception as e:
            logging.error(f"Error fetching webpage content: {e}")
            return None

    def extract_latest_news(self, limit=6):
        page_content = self.fetch_dynamic_webpage_content(self.url)
        if page_content is None:
            return []
        try:
            logging.debug(f"Fetched page content: {page_content[:500]}")  # 输出前500字符进行调试
            soup = BeautifulSoup(page_content, 'html.parser')
            news_list = soup.find('ul', class_='newslist')
            if not news_list:
                logging.warning("未找到新闻内容列表。")
                return []
            news_items = news_list.find_all('li', limit=limit)
            latest_news = []
            for item in news_items:
                date = item.find('div', class_='time').get_text(strip=True).replace('\n', '-')
                title = item.find('div', class_='tit').get_text(strip=True)
                link_tag = item.find('div', class_='tit').find('a')
                link = link_tag['href'] if link_tag else ''
                if link and not link.startswith('http'):
                    link = "https://www.nankai.edu.cn" + link
                latest_news.append({'title': title, 'date': date, 'link': link})
            logging.debug(f"Extracted news: {latest_news}")  # 输出提取的新闻信息进行调试
            return latest_news
        except Exception as e:
            logging.error(f"Error extracting news: {e}")
            return []

    def extract_latest_news2(self, limit=5):
        page_content = self.fetch_dynamic_webpage_content(self.url)
        if page_content is None:
            return []
        try:
            logging.debug(f"Fetched page content: {page_content[:500]}")  # 输出前500字符进行调试
            soup = BeautifulSoup(page_content, 'html.parser')
            news_tables = soup.find_all('table', width="98%", limit=limit)
            if not news_tables:
                logging.warning("未找到新闻内容列表。")
                return []
            yaowen_links = []
            for table in news_tables:
                link_tag = table.find('a')
                date_tag = table.find('div', align="right")
                title = link_tag.get_text(strip=True)
                link = link_tag['href']
                date = date_tag.get_text(strip=True)
                yaowen_links.append({'title': title, 'date': date, 'link': link})
            logging.debug(f"Extracted yaowen links: {yaowen_links}")  # 输出提取的新闻信息进行调试
            return yaowen_links
        except Exception as e:
            logging.error(f"Error extracting Nankai Yaowen links: {e}")
            return []

driver_path = 'edgedriver/msedgedriver.exe'  # 修改为实际路径

urls = {
    "tongzhi": "https://www.nankai.edu.cn/157/list.htm",
    "xiaoqing": "https://www.nankai.edu.cn/159/list.htm",
    "zhuanti": "https://www.nankai.edu.cn/zt/list.htm",
    "yaowen": "https://news.nankai.edu.cn/ywsd/index.shtml",
    "meiti": "https://news.nankai.edu.cn/mtnk/index.shtml"
}

def get_url(t:str):
    if ("要闻" in t):
        type = "yaowen"
    elif ("通知" in t):
        type = "tongzhi"
    elif ("校情" in t):
        type = "xiaoqing"
    elif ("专题" in t):
        type = "zhuanti"
    elif ("媒体" in t):
        type = "meiti"
    else:
        type = "xiaoqing"

    url = urls[type]

    return url,type