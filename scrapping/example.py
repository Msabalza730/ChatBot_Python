from crawl4ai import WebCrawler
from crawl4ai.web_crawler import WebCrawler

crawler = WebCrawler()
crawler.warmup()


url = "https://www.comfenalco.com/contactenos"

result = crawler.run(url)

print(result.markdown)


