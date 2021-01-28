import requests
import argparse
from bs4 import BeautifulSoup
from colorama import Fore, Style
from collections import deque
from urllib.parse import urlparse

class Crawler(object):
    def __init__(self, starting_url, outfile, crawl_depth, extract_forms):
        # Assign submitted parameters to class variables, create empty set for visited sites, and set popular Firefox user agent
        self.starting_url = starting_url
        self.outfile = outfile
        self.crawl_depth = crawl_depth
        self.extract_forms = extract_forms
        self.visited = set([starting_url])
        self.final_links = set()
        self.link_dq = deque([[starting_url, "", 0]])
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"   
    
    def crawl(self, dq):
        # Reference: https://stackoverflow.com/questions/55769347/how-do-i-implement-a-breadth-first-and-depth-first-search-web-crawler

        while dq:
            base, path, depth = dq.popleft()
            #                         ^^^^ removing "left" makes this a DFS (stack)

            if "" in base:  # Can be used to filter for a specific url, otherwise collects all
                if depth < self.crawl_depth:
                    try:
                        soup = BeautifulSoup(requests.get(base + path, headers={"User-Agent":self.user_agent}).text, "html.parser")

                        for link in soup.find_all("a"):
                            href = link.get("href")

                            if href not in self.visited:
                                self.visited.add(href)
                                print("  " * depth + f"at depth {depth}: {href}")

                                if href.startswith("http"):
                                    self.final_links.add(href)
                                    dq.append([href, "", depth + 1])
                                else:
                                    if href.startswith("/"):
                                        self.final_links.add(base + href)
                                        dq.append([base, href, depth + 1])
                                    else:
                                        self.final_links.add(base + "/" + href)
                                        dq.append([base, href, depth + 1])
                    except:
                        print(f"{Fore.RED}Error requesting '{base + path}'{Style.RESET_ALL}")
    
    def extract_forms(self, url):
        # Will fill this in later from the other script
        pass

    def save_output(self, outfile, links):
        # Save the list of links passed in to a file
        try:
            with open(outfile, "w+", encoding="utf-8") as f:
                for link in links:
                    if link is not None:
                        f.write(link + "\n")
        except Exception as e:
            print(f"{Fore.RED}Error writing to file: {e}{Style.RESET_ALL}")
                                
    def start(self):
        # Initialize the crawl of the target site
        

        print(Fore.YELLOW + "\n\n***********************************\n")
        print(Style.RESET_ALL)
        print("[*] Arguments set:")
        print("\tBase URL: {}".format(self.starting_url))
        print("\tCrawl depth: - {}".format(self.crawl_depth))
        print("\tExtract forms? - {}\n".format(self.extract_forms))
        print("[*] Starting crawl of {}\n".format(self.starting_url))
        print(Fore.YELLOW + "***********************************")
        print(Style.RESET_ALL)
        self.crawl(self.link_dq)

        print(Fore.YELLOW + "***********************************\n")
        print(Style.RESET_ALL)
        print("[*] Finished crawl, saving output to '{}'.".format(self.outfile))
        
        if self.outfile:
            self.save_output(self.outfile, self.final_links)


if __name__ == "__main__":
    
    # Create argparse object and set command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", "-u", help="Set target URL", required=True)
    parser.add_argument("--outfile", "-o", help="File to save output to")
    parser.add_argument("--crawl_depth", "-cd", help="Set the depth for crawling the site (Default = 2)", default=2, nargs="?", type=int)
    parser.add_argument("--extract_forms", "-ef", help="Extract forms from target site (Default = False)", default=False, action='store_true')

    # Parse arguments and assign to variables
    args = parser.parse_args()

    url = args.url
    outfile = args.outfile
    crawl_depth = args.crawl_depth
    extract_forms = args.extract_forms

    # Create Crawler object and start the crawl
    crawler = Crawler(url, outfile, crawl_depth, extract_forms)
    crawler.start()