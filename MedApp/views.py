from django.db.models import Count
from django.shortcuts import render

from fusioncharts import FusionCharts
from .models import *


def chart(request):
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Patients by specialization",
        "subCaption": "MedApp Clinic",
        "xAxisName": "Month",
        "yAxisName": "Number of patients",
        "theme": "zune"
    }

    dataSource['data'] = []

    number_patient = Consultation.objects.all().values('specialization').annotate(
        total=Count('specialization')).order_by('total')

    for members in number_patient:
        data = {}
        specilization = Specialization.objects.get(pk=members['specialization'])
        data['label'] = specilization.name

        data['value'] = members['total']
        dataSource['data'].append(data)

    column2D = FusionCharts("column2D", "ex1", "500", "300", "chart-1", "json", dataSource)

    return render(request, 'charts.html', {'output': column2D.render()})
