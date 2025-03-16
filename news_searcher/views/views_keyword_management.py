
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.http import JsonResponse
from news_searcher.models import *
from news_searcher.forms import *
from django.urls import reverse


def keyword_management_index(request):
    records = KeywordRecord.objects.all().order_by("keyword")

    form = KeywordRecordForm()
    if request.method == 'POST':
        if KeywordRecord.objects.filter(keyword=request.POST['keyword']).exists():
            return redirect(reverse('news:keyword_management_index'))
        form = KeywordRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('news:keyword_management_index'))

    return render(request, 'news_searcher/keyword_management/keyword_management_index.html', {"records": records, "form": form})


def keyword_management_edit(request, id):
    record=  KeywordRecord.objects.get(id=id)

    form = KeywordRecordForm(request.POST or None, instance=record)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('news:keyword_management_index'))

    return render(request, 'news_searcher/keyword_management/keyword_management_edit.html', {"form": form})


def keyword_management_delete(request):
    id = request.POST.get('id')
    record = KeywordRecord.objects.get(id=id)
    record.delete()

    return JsonResponse({"Status": "Success"})