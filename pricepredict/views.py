from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'pricepredict/index.html')

def index2(request):
    return render(request, 'pricepredict/main/index-2.html')

