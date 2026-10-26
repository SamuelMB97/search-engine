import requests
import re

class HayStack():
    def __init__(self, url, max_search_deapth=3):
        self.url = url
        self.max_search_deapth = max_search_deapth
        self.index, self.graph = self.crawl_recursive(self.url) # TODO just make crawl_recursive set the variables.
        assert 0
        self.compute_ranks(self.graph)


    def crawl_recursive(self, url, cur_deapth=0):
        """Crawls starting from the given url, indexing words and 
        graphing web links
       
        Crawls starting from the given web page, finding and following 
        all embedded webpage links until it reaches the maximum search 
        depth and computes the following data items:

        1. An index that maps every word encountered on each crawled 
        page to a list of URLs of all the pages that contain that 
        word.
        ex/
        index = {'word': {a, b, c}, 'the': {d, e, f}, 'delight': {g, h}}

        2.A graph that maps every URL encountered to a list of the web 
        pages it links to directly.
        ex/
        graph = {a: {1, 2, 3}, b: {4, 5}}"""
        content = requests.get(url, headers={"User-Agent": "XY"}).text
        print(content)
        
        # Get words
        words = set(self.get_words(content))
        print(words)
    
        # Get links
        links = set(self.get_links(content))
        print(links)


        return (None, None)


    def get_words(self, content):
        no_html = re.sub(r"<.*?>", "", content)
        return re.findall(r"[a-zA-Z]+[a-zA-Z']*", no_html) # TODO double check this pattern

    def get_links(self, content):
        links = re.findall(r"""<a\b[^>]*\bhref\s*=\s*["\']([^"\']*)["\']""", content)
        return links


    def compute_ranks(self, graph):
        """Takes the graph mentioned above and “ranks” the web pages 
        in graph, placing the result in a dictionary, self.ranks, 
        where the key is the url and the value is the page’s rank."""

        d = 0.85     # probability that surfer will bail
        numloops = 10

        ranks = {}
        npages = len(graph)
        for page in graph:
            ranks[page] = 1.0 / npages

        for _ in range(0, numloops):
            newranks = {}
            for page in graph:
                newrank = (1 - d) / npages
                for url in graph:   
                    if page in graph[url]:  # this url links to page
                        newrank += d*ranks[url]/len(graph[url])
                newranks[page] = newrank
            ranks = newranks
        self.ranks = ranks

    def lookup(self, search_key):
        """Takes a word as a search key and outputs the webpages that 
        contain that word in rank order, highest to lowest."""
        pass