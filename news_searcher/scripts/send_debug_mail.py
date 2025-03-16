from news_searcher.lib.news_search_lib import MailGroupManager
from news_searcher.models import MailGroup




def run():
    mail_groups = MailGroup.objects.all()

    for mail_group in mail_groups:
        
        mail_group_manager = MailGroupManager(mail_group.name)
        mail_group_manager.send_debug_mail(2)