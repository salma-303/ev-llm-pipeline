# src/data_collection/scraper.py
import os, logging, requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

class EVWebScraper:
    def __init__(self, base_dir="data/raw"):
        self.logger = logging.getLogger(__name__)
        os.makedirs(base_dir, exist_ok=True)
        self.base_dir = base_dir

    def fetch_with_playwright(self, url: str) -> str:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=30000)
                content = page.content()
                page_text = page.inner_text("body")
                browser.close()
                return page_text
        except Exception as e:
            self.logger.error(f"Playwright scraping failed for {url}: {e}")
            return ""

    def fetch_and_save(self, url: str, filename: str = None):
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36"
                )
            }
            r = requests.get(url, headers=headers, timeout=20)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            content = soup.get_text(separator="\n", strip=True)
        except Exception as e:
            self.logger.warning(f"Standard scraping failed for {url}: {e}")
            content = self.fetch_with_playwright(url)

        if content:
            parsed = urlparse(url)
            name = filename or f"{parsed.netloc.replace('.', '_')}.txt"
            path = os.path.join(self.base_dir, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return path
        else:
            self.logger.error(f"Scraping failed completely for {url}")
            return None
