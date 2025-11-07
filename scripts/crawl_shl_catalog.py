import requests, csv, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.shl.com"

def get_soup(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def extract_product_links():
    url = "https://www.shl.com/solutions/products/product-catalog/"
    soup = get_soup(url)
    links = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(BASE, a["href"])
        if "/product" in href:
            links.add(href)
    return list(links)

def parse_page(url):
    soup = get_soup(url)
    name = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    desc = soup.get_text(separator=" ", strip=True)
    return {"name": name, "url": url, "description": desc}

def main():
    links = extract_product_links()
    print("Found", len(links), "links")
    rows = []
    for link in links:
        try:
            rows.append(parse_page(link))
        except Exception as e:
            print("Error:", e)
        time.sleep(0.5)
    with open("data/shl_catalog_raw.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name","url","description"])
        writer.writeheader()
        writer.writerows(rows)
    print("C:/Users/hp/Desktop/SHL_GenAI_Project/Gen_AI Dataset.xlsx")

if __name__ == "__main__":
    main()
