
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

page_url = "https://dahd.gov.in/node/3273"

response = requests.get(
    page_url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
)

print("Page status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("\nLinks containing BAHS or PDF:")

for link in soup.find_all("a", href=True):
    text = link.get_text(" ", strip=True)
    href = urljoin(page_url, link["href"])

    if "BAHS" in text.upper() or "PDF" in href.upper():
        print("Text:", text)
        print("URL: ", href)
        print("-" * 40)
