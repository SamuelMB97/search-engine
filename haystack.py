import requests
import re

class HayStack():
    def __init__(self, url, max_search_deapth=3):
        self.url = url
        self.max_search_deapth = max_search_deapth

        self.index = dict()
        self.graph = dict()
        self.crawl_recursive(self.url)

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
        #print(content)
        
        # Get words
        words = set(self.get_words(content))
        #print(words)

        for word in words:
            word = word.lower()
            if word in self.index:
                self.index[word].add(url)
            else:
                self.index[word] = {url}
    
        # Get links
        links = set(self.get_links(content))
        #print(links)

        self.graph[url] = set()
        for link in links:
            if link not in self.graph[url]:
                self.graph[url].add(link)

            if cur_deapth <= self.max_search_deapth and \
                link not in self.graph.keys(): # Don't want to crawl a page twice
                self.crawl_recursive(link, cur_deapth=cur_deapth+1)


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
        hits = []
        for url in self.index[search_key.lower()]:# for each url the word shows up in...
            rank = self.ranks[url]
            hits.append((url, rank))
        hits.sort(key=lambda x: x[1], reverse=True)
        return [x[0] for x in hits]
            




