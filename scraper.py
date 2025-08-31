import requests
from bs4 import BeautifulSoup
import time

def scrape_chapter(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    # retry mechanism (3 attempts with small delay)
    for attempt in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            content = soup.find("div", class_="mw-parser-output")
            if not content:
                return "No readable content found."

            text_blocks = []
            for tag in content.find_all(["p", "h2", "h3"]):
                text = tag.get_text(strip=True)
                if text:
                    text_blocks.append(text)

            return "\n\n".join(text_blocks)

        except Exception as e:
            if attempt < 2:
                time.sleep(2)  # wait before retry
            else:
                return f"Error scraping: {e}"
