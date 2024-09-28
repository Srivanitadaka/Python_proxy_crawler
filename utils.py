import logging
import random
import time
from urllib.parse import urlparse, urljoin
from aiohttp import ClientSession

# Set up logging
def setup_logging(log_filename='web_crawler.log'):
    """
    Sets up the logging configuration.

    Args:
    -----
    log_filename (str): The name of the log file.
    """
    logging.basicConfig(filename=log_filename, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging setup complete.")


# URL validation
def is_valid_url(url):
    """
    Checks if a URL is valid and properly formatted.

    Args:
    -----
    url (str): The URL to validate.

    Returns:
    --------
    bool: True if the URL is valid, False otherwise.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


# Function to join relative URLs with the base URL
def make_absolute_url(base_url, link):
    """
    Converts a relative URL into an absolute URL based on the base URL.

    Args:
    -----
    base_url (str): The base URL of the current page.
    link (str): The relative URL to convert.

    Returns:
    --------
    str: The absolute URL.
    """
    return urljoin(base_url, link)


# Randomized delay to avoid hitting rate limits
def random_delay(min_delay=1, max_delay=3):
    """
    Adds a random delay to avoid getting blocked by websites due to rapid requests.

    Args:
    -----
    min_delay (int): Minimum delay in seconds.
    max_delay (int): Maximum delay in seconds.
    """
    delay = random.uniform(min_delay, max_delay)
    logging.info(f"Delaying for {delay:.2f} seconds.")
    time.sleep(delay)


# Check robots.txt compliance (can_fetch method using aiohttp)
async def can_fetch(url, user_agent="*"):
    """
    Checks if a specific user agent is allowed to crawl the page according to robots.txt.

    Args:
    -----
    url (str): The URL to check.
    user_agent (str): The user agent for which the robots.txt should be checked.

    Returns:
    --------
    bool: True if the user agent is allowed to crawl, False otherwise.
    """
    parsed_url = urlparse(url)
    robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", "/robots.txt")
    
    try:
        async with ClientSession() as session:
            async with session.get(robots_url) as response:
                if response.status == 200:
                    text = await response.text()
                    rp = RobotFileParser()
                    rp.parse(text.splitlines())
                    return rp.can_fetch(user_agent, url)
                else:
                    logging.warning(f"Failed to fetch robots.txt for {url} (status code: {response.status})")
    except Exception as e:
        logging.error(f"Error fetching robots.txt for {url}: {str(e)}")
    
    # If robots.txt is not available or there's an error, default to allowing the crawl
    return True


# Extract domain from URL
def get_domain_name(url):
    """
    Extracts and returns the domain name from a given URL.

    Args:
    -----
    url (str): The URL from which to extract the domain.

    Returns:
    --------
    str: The domain name of the URL.
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain.replace('www.', '') if domain else None
    except Exception as e:
        logging.error(f"Failed to extract domain from {url}: {str(e)}")
        return None

