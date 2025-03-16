from news_searcher.lib.news_search_lib import DuckDuckGoNewsSearcher, ChromeDriverManager
from news_searcher.models import KeywordRecord





def run():
    driver = ChromeDriverManager.init_driver()
    dcukduckgo_searher = DuckDuckGoNewsSearcher(driver)
    keyword_records = KeywordRecord.objects.all()
    dcukduckgo_searher.search(keyword_records)  