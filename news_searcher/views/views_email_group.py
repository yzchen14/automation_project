
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.http import JsonResponse

from news_searcher.models import *
from news_searcher.forms import *
from news_searcher.lib.news_search_lib import MailGroupManager
from django.urls import reverse


def mail_group_delete(request):
    mail_group_id = request.POST.get('id')
    mail_group = MailGroup.objects.get(id=mail_group_id)
    mail_group.delete()
    return redirect(reverse('news:mail_group_index'))


def mail_gorup_index(request):
    records = MailGroup.objects.all().order_by("name")
    keyword_records = KeywordRecord.objects.all().order_by("keyword")

    for mail_group in records:
        subscription_records = KeywordRecordSubscription.objects.filter(mail_group=mail_group)
        keyword_list = [subscription.keyword.keyword for subscription in subscription_records]
        mail_group.keyword_list = keyword_list
        mail_group.syn_from_config_file()


    form = MailGroupForm()
    if request.method == 'POST':
        if MailGroup.objects.filter(name=request.POST['name']).exists():
            return redirect(reverse('news:mail_group_index'))
        form = MailGroupForm(request.POST)
        if form.is_valid():
            new_mail_group = form.save()
            new_mail_group.syn_from_config_file()


            return redirect(reverse('news:mail_group_index'))
    cotext = {"records": records, "keyword_records": keyword_records, "form": form}
    return render(request, 'news_searcher/mail_group/mail_group_index.html', cotext)



def mail_group_add_keyword(request):
    mail_group_id = request.POST.get('id')
    keyword_id = request.POST.get('keyword_id')
    subscription_record, created = KeywordRecordSubscription.objects.get_or_create(keyword_id=keyword_id, mail_group_id=mail_group_id)
    subscription_record.save()

    mail_group = MailGroup.objects.get(id=mail_group_id)
    subscription_records = KeywordRecordSubscription.objects.filter(mail_group=mail_group)
    keyword_list = [subscription.keyword.keyword for subscription in subscription_records]
    return JsonResponse({"keyword_list": keyword_list})



def mail_group_delete_keyword(request):
    mail_group_id = request.POST.get('mail_group_id')
    keyword = request.POST.get('keyword')

    subscription_record = KeywordRecordSubscription.objects.get(mail_group_id=mail_group_id, keyword__keyword=keyword)
    subscription_record.delete()

    mail_group = MailGroup.objects.get(id=mail_group_id)
    subscription_records = KeywordRecordSubscription.objects.filter(mail_group=mail_group)
    keyword_list = [subscription.keyword.keyword for subscription in subscription_records]
    return JsonResponse({"keyword_list": keyword_list})