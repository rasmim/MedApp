from django.db.models import Count
from django.shortcuts import render

from fusioncharts import FusionCharts
from .models import *


# The `chart` function is defined to generate Column 2D chart from database.
def chart(request):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Patients by specialization",
        "subCaption": "MedApp Clinic",
        "xAxisName": "Month",
        "yAxisName": "Number of patients",
        "theme": "zune"
    }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.

    number_patient = Consultation.objects.all().values('specialization').annotate(
        total=Count('specialization')).order_by('total')

    for members in number_patient:
        data = {}
        specilization = Specialization.objects.get(pk=members['specialization'])
        data['label'] = specilization.name

        data['value'] = members['total']
        dataSource['data'].append(data)
        # number_patient = Consultation.objects.count(name='specialization')

        # for key in Consultation.objects.all():
        #     data = {}
        #     data['label'] = key.specialization
        #     data['value'] = key.


        # Create an object for the Column 2D chart using the FusionCharts class constructor
    column2D = FusionCharts("column2D", "ex1", "800", "600", "chart-1", "json", dataSource)
    # column2d = FusionCharts()

    return render(request, 'charts.html', {'output': column2D.render()})

# def print_view(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#
#     buffer = BytesIO()
#
#     # Create the PDF object, using the BytesIO object as its "file."
#     p = canvas.Canvas(buffer)
#
#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawImage("medapp.bmp", 5, 750,mask='auto')
#     p.drawCentredString(200,600,"Consultation results")
#
#     # Close the PDF object cleanly.
#     p.showPage()
#     p.save()
#
#     # Get the value of the BytesIO buffer and write it to the response.
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#     return response
