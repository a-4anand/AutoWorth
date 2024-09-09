
from django.shortcuts import render, redirect

# Load the dataset

# Views
def index(request):
    return render(request, 'pricepredict/index.html')



def index2(request):
    return render(request, 'pricepredict/main/index-2.html')



def index3(request):
    return render(request, 'pricepredict/main/index-3.html')



def register(request):
    return render(request, 'pricepredict/main/register.html')

def index6(request):

    return render(request, 'pricepredict/main/index6.html')
