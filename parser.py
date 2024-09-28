from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to parse HTML and extract relevant data
def parse_html(content, base_url):
    """
    Parses the HTML content and extracts the page title and links.
    
    Args:
        content (str): HTML content of the page.
        base_url (str): The base URL of the page to resolve relative links.
    
    Returns:
        tuple: A tuple containing the page title and a set of extracted links.
    """
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract page title
    page_title = soup.title.string.strip() if soup.title else "No Title"
    
    # Extract all valid links from the page
    links = extract_links(soup, base_url)
    
    return page_title, links

# Function to extract all links from the page
def extract_links(soup, base_url):
    """
    Extracts all valid HTTP/HTTPS links from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML using BeautifulSoup.
        base_url (str): Base URL for resolving relative links.

    Returns:
        set: A set of fully qualified URLs extracted from the page.
    """
    links = set()
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        # Resolve relative URLs
        full_url = urljoin(base_url, href)
        # Only add valid HTTP/HTTPS URLs
        if full_url.startswith('http'):
            links.add(full_url)
    return links

# Function to handle JavaScript-rendered content (optional)
def handle_javascript(content):
    """
    Handles JavaScript-rendered content.
    
    Args:
        content (str): HTML content with possible JavaScript-rendered data.
    
    Returns:
        str: Extracted data (stub function for expansion).
    """
    # Placeholder for dealing with JavaScript-rendered pages using libraries like Selenium or Playwright
    return content

# Function to sanitize and normalize content
def sanitize_content(content):
    """
    Sanitizes and normalizes HTML content for further processing.

    Args:
        content (str): Raw HTML content of the page.

    Returns:
        str: Cleaned and normalized HTML content.
    """
    # Remove excessive whitespace, normalize line breaks, etc.
    return ' '.join(content.split()).strip()
