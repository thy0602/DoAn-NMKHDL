from crawler import Crawler

if __name__ == '__main__':
  crawler = Crawler()

  producers = ["apple", "lenovo"]

  crawler.crawl(producers = producers)

  crawler.crawl_with_custom_config(producers = producers)
