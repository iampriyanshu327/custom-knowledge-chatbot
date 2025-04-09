
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# import tldextract
# import time

# def is_valid_url(url):
#     try:
#         parsed = urlparse(url)
#         return parsed.scheme in ('http', 'https')
#     except:
#         return False

# def is_internal_url(base_url, target_url):
#     base_domain = tldextract.extract(base_url).domain
#     target_domain = tldextract.extract(target_url).domain
#     return base_domain == target_domain

# def get_all_links(base_url, html):
#     soup = BeautifulSoup(html, "html.parser")
#     links = set()
#     for tag in soup.find_all("a", href=True):
#         full_url = urljoin(base_url, tag['href'])
#         if is_valid_url(full_url) and is_internal_url(base_url, full_url):
#             links.add(full_url)
#     return links

# # def extract_text_from_html(html):
# #     soup = BeautifulSoup(html, "html.parser")
# #     for script in soup(["script", "style", "noscript"]):
# #         script.extract()
# #     return soup.get_text(separator=' ', strip=True)

# def extract_text_from_html(html):
#     soup = BeautifulSoup(html, "html.parser")
#     for script in soup(["script", "style", "noscript"]):
#         script.extract()

#     text = soup.get_text(separator=' ', strip=True)
#     extras = []

#     # Extract founding date
#     founding = soup.find("dd", class_="order-first text-xl font-bold tracking-tight text-gray-900 lg:text-3xl xl:text-5xl")
#     if founding:
#         extras.append(f"Founding Date: {founding.text.strip()}")

#     # Extract Instagram link
#     insta = soup.find("a", href=True, string=lambda s: s and "Instagram" in s)
#     if insta:
#         extras.append(f"Instagram URL: {insta['href']}")

#     return text + "\n\n" + "\n".join(extras)

# def crawl_website(start_url, max_pages=20, delay=1):
#     visited = set()
#     to_visit = {start_url}
#     text_data = {}

#     while to_visit and len(visited) < max_pages:
#         url = to_visit.pop()
#         if url in visited:
#             continue

#         print(f"Crawling: {url}")
#         try:
#             response = requests.get(url, timeout=10)
#             response.raise_for_status()
#             html = response.text

#             page_text = extract_text_from_html(html)
#             text_data[url] = page_text

#             new_links = get_all_links(start_url, html)
#             to_visit.update(new_links - visited)
#             visited.add(url)

#             time.sleep(delay) # to disallow interuption in servers!

#         except Exception as e:
#             print(f"Failed to fetch {url}: {e}")

#     return text_data

# if __name__ == "__main__":
#     domain = "https://pageupsoft.com"
#     crawled_data = crawl_website(domain)

#     with open("raw_text_data.txt", "w", encoding="utf-8") as f:
#         for url, text in crawled_data.items():
#             f.write(f"URL: {url}\n{text}\n\n{'='*80}\n\n")

#     print(f"\nCrawled {len(crawled_data)} pages. Data saved to 'raw_text_data.txt'.")







# # import requests
# # from bs4 import BeautifulSoup
# # from urllib.parse import urljoin, urlparse
# # import tldextract
# # import time
# # import re

# # def is_valid_url(url):
# #     try:
# #         parsed = urlparse(url)
# #         return parsed.scheme in ('http', 'https')
# #     except:
# #         return False

# # def is_internal_url(base_url, target_url):
# #     base_domain = tldextract.extract(base_url).domain
# #     target_domain = tldextract.extract(target_url).domain
# #     return base_domain == target_domain

# # def get_all_links(base_url, html):
# #     soup = BeautifulSoup(html, "html.parser")
# #     links = set()
# #     for tag in soup.find_all("a", href=True):
# #         full_url = urljoin(base_url, tag['href'])
# #         if is_valid_url(full_url) and is_internal_url(base_url, full_url):
# #             links.add(full_url)
# #     return links

# # def extract_text_from_html(html):
# #     soup = BeautifulSoup(html, "html.parser")
# #     for script in soup(["script", "style", "noscript"]):
# #         script.extract()

# #     text = soup.get_text(separator=' ', strip=True)
# #     extras = []

# #     # --- Smart extraction from all tags ---

# #     # 📌 Extract any years like 2016, 2020, etc.
# #     years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
# #     if years:
# #         extras.append(f"Founding Year (guessed): {min(years)}")

# #     # 📌 Extract Instagram, LinkedIn, etc.
# #     for a in soup.find_all("a", href=True):
# #         href = a['href']
# #         if "instagram.com" in href:
# #             extras.append(f"Instagram: {href}")
# #         if "linkedin.com" in href:
# #             extras.append(f"LinkedIn: {href}")
# #         if "facebook.com" in href:
# #             extras.append(f"Facebook: {href}")
# #         if "twitter.com" in href:
# #             extras.append(f"Twitter: {href}")

# #     # 📌 Extract emails
# #     emails = set(re.findall(r"[\w\.-]+@[\w\.-]+", text))
# #     if emails:
# #         for email in emails:
# #             extras.append(f"Email: {email}")

# #     # 📌 Extract phone numbers
# #     phones = set(re.findall(r"\+?\d[\d\s\-()]{7,}\d", text))
# #     if phones:
# #         for phone in phones:
# #             extras.append(f"Phone: {phone}")

# #     return text + "\n\n" + "\n".join(extras)

# # def crawl_website(start_url, max_pages=20, delay=1):
# #     visited = set()
# #     to_visit = {start_url}
# #     text_data = {}

# #     while to_visit and len(visited) < max_pages:
# #         url = to_visit.pop()
# #         if url in visited:
# #             continue

# #         print(f"Crawling: {url}")
# #         try:
# #             response = requests.get(url, timeout=10)
# #             response.raise_for_status()
# #             html = response.text

# #             page_text = extract_text_from_html(html)
# #             text_data[url] = page_text

# #             new_links = get_all_links(start_url, html)
# #             to_visit.update(new_links - visited)
# #             visited.add(url)

# #             time.sleep(delay) # to disallow interruption in servers!

# #         except Exception as e:
# #             print(f"Failed to fetch {url}: {e}")

# #     return text_data

# # if __name__ == "__main__":
# #     domain = "https://pageupsoft.com"
# #     crawled_data = crawl_website(domain)

# #     with open("raw_text_data.txt", "w", encoding="utf-8") as f:
# #         for url, text in crawled_data.items():
# #             f.write(f"URL: {url}\n{text}\n\n{'='*80}\n\n")

# #     print(f"\nCrawled {len(crawled_data)} pages. Data saved to 'raw_text_data.txt'.")


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
import time
import re

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https')
    except:
        return False

def is_internal_url(base_url, target_url):
    base_domain = tldextract.extract(base_url).domain
    target_domain = tldextract.extract(target_url).domain
    return base_domain == target_domain

def get_all_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        full_url = urljoin(base_url, tag['href'])
        if is_valid_url(full_url) and is_internal_url(base_url, full_url):
            links.add(full_url)
    return links

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style", "noscript"]):
        script.extract()

    text = soup.get_text(separator=' ', strip=True)
    extras = []

    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    if years:
        extras.append(f"Founding Year (guessed): {min(years)}")

    social_domains = {
        "instagram.com": "Instagram",
        "linkedin.com": "LinkedIn",
        "facebook.com": "Facebook",
        "twitter.com": "Twitter",
        "youtube.com": "YouTube",
        "youtu.be": "YouTube"
    }
    for a in soup.find_all("a", href=True):
        href = a['href']
        for domain, label in social_domains.items():
            if domain in href:
                extras.append(f"{label}: {href}")

    emails = set(re.findall(r"[\w\.-]+@[\w\.-]+", text))
    if emails:
        for email in emails:
            extras.append(f"Email: {email}")

    phones = set(re.findall(r"\+?\d[\d\s\-()]{7,}\d", text))
    if phones:
        for phone in phones:
            extras.append(f"Phone: {phone}")

    for dt in soup.find_all("dt"):
        label = dt.get_text(strip=True)
        dd = dt.find_next_sibling("dd")
        if dd:
            value = dd.get_text(strip=True)
            extras.append(f"{label}: {value}")

    return text + "\n\n" + "\n".join(extras)

def crawl_website(start_url, max_pages=20, delay=1):
    visited = set()
    to_visit = {start_url}
    text_data = {}

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue

        print(f"Crawling: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html = response.text

            page_text = extract_text_from_html(html)
            text_data[url] = page_text

            new_links = get_all_links(start_url, html)
            to_visit.update(new_links - visited)
            visited.add(url)

            time.sleep(delay) # to disallow interruption in servers!

        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    return text_data

if __name__ == "__main__":
    domain = "https://pageupsoft.com"
    crawled_data = crawl_website(domain)

    with open("raw_text_data.txt", "w", encoding="utf-8") as f:
        for url, text in crawled_data.items():
            f.write(f"URL: {url}\n{text}\n\n{'='*80}\n\n")

    print(f"\nCrawled {len(crawled_data)} pages. Data saved to 'raw_text_data.txt'.")
