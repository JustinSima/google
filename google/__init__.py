""" A class for searching Google inspired by the googlesearch package: https://github.com/Nv7-GitHub/googlesearch."""
import time
import random
import urllib

from bs4 import BeautifulSoup
import requests


class Google:
    """ Search Google for top results for a given term, returns the url's."""
    def __init__(self, num_results: int, sleep_interval: int, timeout: int):
        self.num_results = num_results
        self.sleep_interval = sleep_interval
        self.timeout = timeout
        
        self._useragent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
        ]
    
    def _get_useragent(self):
        return random.choice(self._useragent_list)
    
    def _request(self, term: str, start: int):
        response = requests.get(
            url="https://www.google.com/search",
            headers={"User-Agent": self._get_useragent()},
            params={
                "q": term,
                "num": self.num_results - start + 2,
                "hl": 'en',
                "start": start,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()

        return response
    
    def search(self, term: str):
        """ Search Google for the given term and return the returned url's."""
        escaped_term = urllib.parse.quote_plus(term) # make 'site:xxx.xxx.xxx ' works.

        # Fetch
        results = []
        start = 0
        while start < self.num_results:
            # Get response.
            response = self._request(escaped_term, start)

            # Parse response.
            soup = BeautifulSoup(response.text, "html.parser")
            result_block = soup.find_all("div", attrs={"class": "g"})

            if len(result_block) == 0:
                start += 1

            for result in result_block:
                link = result.find("a", href=True)
                title = result.find("h3")
                
                if link and title:
                    start += 1
                    results.append(link["href"])

            time.sleep(self.sleep_interval)

            if start == 0:
                break
        
        return results

    def advanced_search(self, term: str):
        """ Search Google for the given term and return request responses for the returned url's."""
        urls = self.search(term)
        responses = [requests.get(url, headers={"User-Agent": self._get_useragent()}, timeout=self.timeout) for url in urls]
        
        return responses
