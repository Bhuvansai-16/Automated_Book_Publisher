import requests
from bs4 import BeautifulSoup

def scrape_chapter(url: str) -> str:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find("div", class_="mw-parser-output")
        if not content:
            return "No readable content found."
        return "\n\n".join([p.get_text(strip=True) for p in content.find_all(["p", "h2", "h3"])])
    except Exception as e:
        return f"Error scraping: {e}"
