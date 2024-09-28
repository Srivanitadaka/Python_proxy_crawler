import random
import aiohttp
import logging

# Set up logging
logging.basicConfig(filename='proxy_manager.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyManager:
    """
    A class to manage proxy rotation and validation for web crawling.

    Attributes:
    ------------
    proxies : list
        A list of available proxies.
    validated_proxies : list
        A list of validated working proxies.
    test_url : str
        A URL to test if the proxies work properly.

    Methods:
    --------
    get_random_proxy():
        Returns a random proxy from the validated list.
    validate_proxies():
        Validates the available proxies by checking if they work.
    """
    
    def __init__(self, proxies=None, test_url="https://httpbin.org/ip"):
        """
        Initializes ProxyManager with a list of proxies and a test URL.

        Args:
        -----
        proxies (list): A list of proxy URLs in the format 'http://username:password@proxy.com:port'.
        test_url (str): The URL used to test proxy validity.
        """
        self.proxies = proxies or []
        self.validated_proxies = []
        self.test_url = test_url

    async def get_random_proxy(self):
        """
        Returns a random proxy from the validated proxies list.

        Returns:
        --------
        str: A randomly selected working proxy URL.
        """
        if not self.validated_proxies:
            logging.error("No validated proxies available.")
            return None
        return random.choice(self.validated_proxies)

    async def validate_proxy(self, proxy, session):
        """
        Validates a single proxy by making a request to the test URL.

        Args:
        -----
        proxy (str): The proxy URL to be validated.
        session (aiohttp.ClientSession): The session used to test the proxy.

        Returns:
        --------
        bool: True if the proxy is valid, False otherwise.
        """
        try:
            async with session.get(self.test_url, proxy=proxy, timeout=10) as response:
                if response.status == 200:
                    logging.info(f"Proxy {proxy} is valid.")
                    return True
        except Exception as e:
            logging.warning(f"Proxy {proxy} failed: {str(e)}")
        return False

    async def validate_proxies(self):
        """
        Validates all available proxies by checking if they work with the test URL.
        Stores validated proxies in the validated_proxies list.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.validate_proxy(proxy, session) for proxy in self.proxies]
            results = await asyncio.gather(*tasks)

        self.validated_proxies = [proxy for proxy, valid in zip(self.proxies, results) if valid]

        logging.info(f"Validated proxies: {self.validated_proxies}")
        if not self.validated_proxies:
            logging.error("No working proxies found.")

# Example usage
if __name__ == "__main__":
    proxies = [
        "http://user:pass@proxy1.com:8080",
        "http://user:pass@proxy2.com:8080",
        # Add more proxies here
    ]
    
    proxy_manager = ProxyManager(proxies)

    # Run validation asynchronously
    loop = asyncio.get_event_loop()
    loop.run_until_complete(proxy_manager.validate_proxies())

    # Get a random working proxy
    loop.run_until_complete(proxy_manager.get_random_proxy())
