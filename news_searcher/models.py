import configparser
from django.db import models
from loguru import logger
from django.conf import settings
import os



class KeywordRecord(models.Model):
    keyword = models.TextField(blank=True)  # String for search or crawling purposes
    correlation_words = models.TextField(blank=True)
    description = models.TextField(blank=True)  # Optional description of the group


class NewsRecord(models.Model):
    title = models.CharField(max_length=300)  # Title of the news record
    link = models.URLField()  # URL link to the full news article
    source = models.CharField(max_length=255)  # Source name or website of the article
    file_location = models.TextField(blank=True, null=True)  # Path to the file (optional)
    doi_id = models.CharField(max_length=255, blank=True, null=True)
    affiliation = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)



class CorrelationRecord(models.Model):
    news_record = models.ForeignKey(NewsRecord, on_delete=models.CASCADE)
    keyword_record = models.ForeignKey(KeywordRecord, on_delete=models.CASCADE)


class MailGroup(models.Model):
    name = models.CharField(max_length=255)  # The name of the subscription group
    email_list = models.TextField(default="[]")  # A list of email addresses, stored as a text
    main_group = models.CharField(max_length=15, blank=True, null=True)
    level = models.IntegerField(default=1)

    def get_email_list(self):
        return eval(self.email_list)

    def get_config_file(self):
        email_group_folder = os.path.join(settings.MAIL_GROUP_CONFIG_FOLDER, self.name)
        os.makedirs(email_group_folder, exist_ok=True)
        return os.path.join(email_group_folder, f"{self.name}.ini")

    def syn_from_config_file(self):
        config_file = self.get_config_file()
        if not os.path.exists(config_file):
            logger.debug("No config file found, creating with default settings")
            self.create_config_file(config_file)
        else:
            config = configparser.ConfigParser()
            config.read(config_file)
            email_list = config.get("MailGroup", "email_list")
            level = config.getint("MailGroup", "level")

            self.email_list = email_list
            self.level = int(level)
            self.save()

    def create_config_file(self, config_file):
        config = configparser.ConfigParser()
        config.add_section("MailGroup")
        config.set("MailGroup", "name", self.name)
        config.set("MailGroup", "email_list", "[]")
        config.set("MailGroup", "level", "1")
        with open(config_file, "w") as f:
            config.write(f)


class KeywordRecordSubscription(models.Model):
    keyword = models.ForeignKey(KeywordRecord, on_delete=models.CASCADE, null=True)
    mail_group = models.ForeignKey(MailGroup, on_delete=models.CASCADE, null=True)


class ExclusionSiteRecord(models.Model):
    site = models.CharField(max_length=255)

    def __str__(self):
        return self.site