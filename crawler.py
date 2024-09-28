import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import logging
from urllib.robotparser import RobotFileParser
from fake_useragent import UserAgent

# Set up logging
logging.basicConfig(filename='web_crawler.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Fake user agent for rotating User-Agent header
ua = UserAgent()

# Set of visited URLs to avoid duplication
visited_urls = set()

# Proxy support (optional)
proxies = [
    "http://proxy1.com:8080",
    "http://proxy2.com:8080",
    # Add more proxies here if available
]

# Function to check robots.txt for permission to crawl
def can_fetch(url):
    robots_url = urljoin(url, '/robots.txt')
    rp = RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch('*', url)
    except:
        return True  # Default to allow if robots.txt cannot be read

# Function to extract links from a page
def extract_links(soup, base_url):
    links = set()
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        full_url = urljoin(base_url, href)
        if full_url.startswith('http') and full_url not in visited_urls:
            links.add(full_url)
    return links

# Asynchronous crawler function
async def crawl(url, session, max_depth, current_depth=0):
    if current_depth > max_depth or url in visited_urls:
        return

    visited_urls.add(url)

    # Respect robots.txt rules
    if not can_fetch(url):
        logging.info(f"Blocked by robots.txt: {url}")
        return

    # Set up headers with a rotating User-Agent
    headers = {"User-Agent": ua.random}
    
    # Use proxy rotation (optional)
    proxy = random.choice(proxies) if proxies else None

    try:
        async with session.get(url, headers=headers, proxy=proxy, timeout=10) as response:
            if response.status != 200:
                logging.warning(f"Failed to access {url} (Status code: {response.status})")
                return

            # Parse the page using BeautifulSoup
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')

            # Extract the page title
            page_title = soup.title.string if soup.title else "No Title"
            logging.info(f"Crawled URL: {url} | Title: {page_title}")

            # Extract links and schedule recursive crawling
            links = extract_links(soup, url)
            tasks = [crawl(link, session, max_depth, current_depth + 1) for link in links]

            await asyncio.gather(*tasks)

            # Rate limiting with random delay to avoid server overload
            await asyncio.sleep(random.uniform(1, 2))

    except Exception as e:
        logging.error(f"Error crawling {url}: {str(e)}")

# Function to handle all asynchronous crawling tasks
async def fetch_all(urls, max_depth):
    async with aiohttp.ClientSession() as session:
        tasks = [crawl(url, session, max_depth) for url in urls]
        await asyncio.gather(*tasks)

# Main function to start the crawler
def start_crawler(start_urls, max_depth=2):
    # Start the asyncio event loop
    asyncio.run(fetch_all(start_urls, max_depth))

# Run the crawler if this script is executed
if __name__ == "__main__":
    # Initial URLs to start crawling
    start_urls = [
        "https://example.com",
        "https://another-example.com"
    ]

    # Set the maximum depth for crawling
    max_depth = 2

    # Start crawling
    start_crawler(start_urls, max_depth)

    logging.info("Crawling completed.")
