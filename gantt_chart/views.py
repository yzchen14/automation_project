
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.http import JsonResponse
from django.urls import reverse
from gantt_chart.lib.gantt_chart_lib import *



def gantt_chart_index(request):
    return render(request, 'gantt_chart/gantt_chart_index.html')



def fetchJsonData(request):
    manager = GanttChartManager( pd.Timestamp.now() - pd.Timedelta(days=1), pd.Timestamp.now())
    manager.get_data()
    data = manager.get_json_of_data()

    return JsonResponse({"Status": "OK", "data": data})