import argparse
import json
import sys
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False

def crawl(url: str, max_links: int = 10):
    if not is_valid_url(url):
        print(json.dumps({"error": "Invalid URL format. Must start with http:// or https://"}), file=sys.stderr)
        sys.exit(1)

    try:
        headers = {"User-Agent": "BuildSprint-CLI-Bot/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Failed to fetch URL: {str(e)}"}), file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.title.string.strip() if soup.title and soup.title.string else "No title"
    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"]) if h.get_text(strip=True)][:10]
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 40][:5]
    links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http")][:max_links]

    result = {
        "status": "success",
        "url": url,
        "http_status": response.status_code,
        "title": title,
        "meta_description": meta_desc,
        "headings": headings,
        "key_content": paragraphs,
        "external_links": links
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Safe CLI Web Crawler")
    parser.add_argument("--url", required=True, help="Target URL to crawl")
    parser.add_argument("--max-links", type=int, default=10, help="Max links to extract")
    args = parser.parse_args()
    crawl(args.url, args.max_links)