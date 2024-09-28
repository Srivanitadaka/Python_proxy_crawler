Web Crawler Package
===================
This package provides functionality to perform asynchronous web crawling, extract data from HTML, and
handle features such as user-agent spoofing, proxy rotation, and robots.txt compliance.

Modules:
--------
- crawler: Contains the main logic for web crawling.
"""

from .crawler import start_crawler

__all__ = ['start_crawler']
__version__ = "1.0.0"
