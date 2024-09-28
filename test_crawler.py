import unittest
import asyncio
from utils import is_valid_url, make_absolute_url, get_domain_name, can_fetch
from proxy_manager import ProxyManager
from aiohttp import ClientSession

class TestWebCrawlerUtils(unittest.TestCase):
    
    def test_is_valid_url(self):
        """Test URL validation functionality."""
        valid_url = "https://example.com"
        invalid_url = "invalid_url"
        
        self.assertTrue(is_valid_url(valid_url))
        self.assertFalse(is_valid_url(invalid_url))
    
    def test_make_absolute_url(self):
        """Test conversion of relative URLs to absolute URLs."""
        base_url = "https://example.com"
        relative_link = "/about"
        absolute_url = make_absolute_url(base_url, relative_link)
        
        self.assertEqual(absolute_url, "https://example.com/about")
    
    def test_get_domain_name(self):
        """Test domain name extraction."""
        url = "https://www.example.com/about"
        domain = get_domain_name(url)
        
        self.assertEqual(domain, "example.com")
    
    def test_make_absolute_url_no_relative(self):
        """Test absolute URL when the link is already absolute."""
        base_url = "https://example.com"
        absolute_link = "https://example.com/about"
        result = make_absolute_url(base_url, absolute_link)
        
        self.assertEqual(result, "https://example.com/about")


class TestProxyManager(unittest.TestCase):
    
    def setUp(self):
        """Set up ProxyManager with sample proxies."""
        self.proxy_list = [
            "http://user:pass@proxy1.com:8080",
            "http://user:pass@proxy2.com:8080"
        ]
        self.proxy_manager = ProxyManager(proxies=self.proxy_list)
    
    def test_initial_proxy_list(self):
        """Test if ProxyManager initializes with the correct proxy list."""
        self.assertEqual(len(self.proxy_manager.proxies), 2)
    
    def test_get_random_proxy(self):
        """Test if ProxyManager can return a valid random proxy."""
        asyncio.run(self.proxy_manager.validate_proxies())
        random_proxy = asyncio.run(self.proxy_manager.get_random_proxy())
        
        self.assertIsNotNone(random_proxy)
        self.assertIn(random_proxy, self.proxy_manager.validated_proxies)


class TestRobotsTxt(unittest.TestCase):

    async def fetch_robots_check(self, url):
        """Helper async function to test robots.txt."""
        return await can_fetch(url)

    def test_robots_txt_allowed(self):
        """Test if robots.txt allows access to a certain URL."""
        url = "https://httpbin.org"
        result = asyncio.run(self.fetch_robots_check(url))
        
        self.assertTrue(result)
    
    def test_robots_txt_disallowed(self):
        """Test if robots.txt disallows access to a certain URL."""
        url = "https://example.com/some-restricted-path"
        result = asyncio.run(self.fetch_robots_check(url))
        
        # This assumes the robots.txt disallows the path. Adjust based on your expectations.
        self.assertFalse(result)


# Asynchronous test class for web crawling
class TestCrawler(unittest.TestCase):

    async def mock_crawl(self, url):
        """Mock crawling function to simulate real crawling."""
        async with ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        return True
            except:
                return False
        return False

    def test_crawl_valid_url(self):
        """Test if crawling a valid URL succeeds."""
        url = "https://example.com"
        result = asyncio.run(self.mock_crawl(url))
        self.assertTrue(result)

    def test_crawl_invalid_url(self):
        """Test if crawling an invalid URL fails."""
        url = "https://invalid-url.fake"
        result = asyncio.run(self.mock_crawl(url))
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
