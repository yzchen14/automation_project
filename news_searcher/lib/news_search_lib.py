import os
import re
import time
import json
import hashlib
import urllib
import configparser
import datetime

from bs4 import BeautifulSoup
from loguru import logger
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from django.conf import settings
from tqdm import tqdm
from news_searcher.models import *
from django.template import loader

class NewsStorageManager:
    def __init__(self, archive_folder=None):
        if archive_folder is None:
            archive_folder = settings.MAIL_ARCHIVE_FOLDER
            
        self.archive_folder = archive_folder
        os.makedirs(self.archive_folder, exist_ok=True)

    def save_news(self, news_list, keyword_record):
        for news in news_list:
            news_record, created = NewsRecord.objects.get_or_create(title=news["title"])
            if created:
                temp = news.copy()
                temp["date"] = news["date"].strftime("%Y-%m-%d %H:%M:%S")
                filename = hashlib.md5(news["title"].encode()).hexdigest()
                file_location = os.path.join(self.archive_folder, f"{filename}.json")

                with open(file_location, "w", encoding="utf-8") as f:
                    json.dump(temp, f)

                news_record.link = news["link"]
                news_record.source = news["source"]
                news_record.file_location = file_location
                news_record.date = news["date"]
                news_record.save()

            self.create_correlation_record(news_record, keyword_record)

    @staticmethod
    def create_correlation_record(news_record, keyword_record):
        correlation_record, created = CorrelationRecord.objects.get_or_create(
            news_record=news_record, keyword_record=keyword_record
        )
        if created:
            correlation_record.save()


class DuckDuckGoNewsSearcher:
    def __init__(self, driver, archive_folder="NewsArchive"):
        self.driver = driver
        self.exlusion_sites = list(
            ExclusionSiteRecord.objects.all().values_list("site", flat=True)
        )
        self.storage_manager = NewsStorageManager(archive_folder)

    def search(self, keyword_records):
        for keyword_record in keyword_records:
            # logger.debug(f"Search keyword: \033[31m{keyword_record}\033[39m")
            keyword = keyword_record.keyword
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"https://duckduckgo.com/?q={encoded_keyword}&t=h_&df=d&iar=news&ia=news"
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "result__title"))
                )
            except:
                logger.debug("No news found")
                continue

            news_list = self.extract_news(keyword_record)
            news_list = self.filter_with_exclusion_set(news_list)
            news_list = self.filter_news_list_with_keyword(news_list, keyword_record)
            news_list = self.get_news_content(news_list)
            news_list = self.summarize_news(news_list)
            self.storage_manager.save_news(news_list, keyword_record)

    def extract_news(self, keyword_record):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        news_list = soup.find_all("div", class_="result--news")
        titles = [news.find(class_="result__a").text for news in news_list]

        existing_news = NewsRecord.objects.filter(title__in=titles)
        existing_news_dict = {news.title: news for news in existing_news}

        news_result = []
        for news in news_list:
            title = news.find(class_="result__a").text
            # check if the news is already in the database
            if title in existing_news_dict:
                news_record = existing_news_dict[title]
                self.storage_manager.create_correlation_record(
                    news_record, keyword_record
                )
                continue

            link = news.get("data-link")
            source = news.find_all(class_="result__url")[0].text
            time_s = self.convert_relative_date(
                news.find_all(class_="result__timestamp")[0].text
            )
            temp = {
                "title": title,
                "link": link,
                "date": time_s,
                "source": source,
                "keyword": keyword_record.keyword,
            }
            news_result.append(temp)

        logger.debug(
            f"News found: {len(news_result)} with [\033[32m{keyword_record.keyword}\033[39m]"
        )
        return news_result

    def filter_with_exclusion_set(self, news_list):
        temp_list = []
        for news in news_list:
            if any(site in news["link"] for site in self.exlusion_sites):
                continue
            temp_list.append(news)

        logger.debug(f"News after filtering with exclusion set: {len(temp_list)}")
        return temp_list

    def filter_news_list_with_keyword(self, news_list, keyword):

        return news_list

    def convert_relative_date(self, relative_date):
        now = datetime.now()
        if "hour" in relative_date:
            hours_ago = int(re.search(r"(\d+)", relative_date).group(1))
            date_time = now - timedelta(hours=hours_ago)
        elif "minute" in relative_date:
            minutes_ago = int(re.search(r"(\d+)", relative_date).group(1))
            date_time = now - timedelta(minutes=minutes_ago)
        elif "day" in relative_date:
            days_ago = int(re.search(r"(\d+)", relative_date).group(1))
            date_time = now - timedelta(days=days_ago)
        else:
            date_time = now
        return date_time

    def get_news_content(self, news_list):
        with tqdm(news_list, desc="Extracting", ncols=100, dynamic_ncols=True) as pbar:
            for news in pbar:
                pbar.set_postfix(title=news["title"], refresh=True)
                self.driver.get(news["link"])
                time.sleep(6)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                news["content"] = re.sub(r"\n+", "\n", soup.body.get_text())
        return news_list

    def summarize_news(self, news_list):

        return news_list




class ChromeDriverManager:

    @staticmethod
    def init_driver():
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Run in headless mode (no UI)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure")
        options.add_argument('--disable-notifications')

        # Initialize the WebDriver
        driver = webdriver.Chrome(options=options)

        return driver



class MailGroupManager:
    def __init__(self, name="EUVL"):
        self.name = name
        self.record = MailGroup.objects.get(name=name)


    def send_debug_mail(self, nums_days = 1):
        logger.debug(f"Sending debug mail for {self.name}")
        self.get_news(num_days=nums_days)
        email_list = ['']



    def send_mail_formal(self, nums_days = 1):
        if datetime.now().hour != 7:
            logger.error(f"It is {datetime.now().hour}:00, not sending the mail")
            return
        
        logger.debug(f"Sending formal mail for {self.name}")
        self.get_news(num_days=nums_days)
        email_list = self.record.get_email_list()
        html_content = self.render_mail()
        self.send_email_with_outlook(html_content, email_list)
        self.generate_send_record(self.news_records)


    def get_news(self, num_days):
        self.keyword_records = [x.keyword for x in KeywordRecordSubscription.objects.filter(mail_group=self.record)]
        print("Keyword records: ", [x.keyword for x in self.keyword_records])
        self.news_records = CorrelationRecord.objects.filter(
            keyword_record__in=self.keyword_records,
            news_record__date__gte=datetime.now() - timedelta(days=num_days)
        ).all()
        self.get_correlation_keywords_for_news_records()
        self.fetch_summarization_data()
        logger.debug(f"Total news records: " + str(len(self.news_records)))



    def get_correlation_keywords_for_news_records(self):
        for news_record in self.news_records:
            news_record.keyword_list = CorrelationRecord.objects.filter(
                news_record=news_record,
                keyword_record__in=self.keyword_records
            ).all()
            

    def fetch_summarization_data(self):
        for news_record in self.news_records:
            with open(news_record.file_location, "r", encoding="utf-8") as f:
                data = json.load(f)
            news_record.summarization_data = data


    def render_mail(self):
        t = loader.get_template("news_searcher/email_template.html")
        html_content = t.render({"records": self.news_records})
        return html_content
    



    def send_email_with_outlook(self, html_content, email_list):
        pass


    def generate_send_record(self, news_records):
        for news_record in news_records:
            send_record, created = NewsSendRecord.objects.get_or_create(mail_group_name=self.name, news_record=news_record)
            if created:
                send_record.save()

