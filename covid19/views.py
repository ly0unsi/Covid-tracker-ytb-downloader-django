from django.shortcuts import render
import requests
from .models import*
from .forms import emailForm
from django.contrib import messages
import ffmpeg
# Create your views here.


def index(request):

    result = None
    globalSummary = None
    emailForm = None
    result = requests.get('https://api.covid19api.com/summary')
    result2 = requests.get(
        'https://opendata.arcgis.com/datasets/454f46db2cfd49fca37245541810d18b_6.geojson')
    json = result.json()
    globalSummary = json['Global']
    countries = json['Countries']
    data = True

    if request.method == 'POST':
        emailForm = emailForm(request.POST)
        if emailForm.is_valid():
            emailForm.save()
            messages.success(request, "Done")

    context = {'globalSummary': globalSummary,
               'countries': countries, 'emailForm': emailForm}
    return render(request, 'dashboard.html', context)
