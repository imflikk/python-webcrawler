# python-webcrawler
Python Web Crawler using a breadth-first search with several parameters to tailor the behavior.

Usage: crawler.py [-h] --url URL [--outfile OUTFILE] [--crawl_depth [CRAWL_DEPTH]] [--extract_forms]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     Set target URL
  --outfile OUTFILE, -o OUTFILE
                        File to save output to
  --crawl_depth [CRAWL_DEPTH], -cd [CRAWL_DEPTH]
                        Set the depth for crawling the site (Default = 2)
  --extract_forms, -ef  Extract forms from target site (Default = False)
  
Example Usage:
  python crawler.py --url https://www.google.com --crawl-depth 1 --extract-forms --outfile google-crawl.txt
