
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.http import JsonResponse

from news_searcher.models import *
from news_searcher.forms import *
from django.urls import reverse

def exclusion_site_management_index(request):
    records = ExclusionSiteRecord.objects.all().order_by("site")

    form = ExclusionSiteRecordForm()
    if request.method == 'POST':
        if ExclusionSiteRecord.objects.filter(site=request.POST['site']).exists():
            return redirect(reverse('news:exclusion_site_management_index'))
        form = ExclusionSiteRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('news:exclusion_site_management_index'))

    return render(request, 'news_searcher/exclusion_site_management/exclusion_site_management_index.html', {"records": records, "form": form})


def exclusion_site_management_delete(request):
    id = request.POST.get('id')
    record = ExclusionSiteRecord.objects.get(id=id)
    record.delete()

    return JsonResponse({"Status": "Success"})