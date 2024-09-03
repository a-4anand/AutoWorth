
import pandas as pd

from .forms import PredictionForm
import pickle
from .forms import PredictionForm

from django.http import JsonResponse
import joblib



# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'pricepredict/index.html')

def index2(request):
    return render(request, 'pricepredict/main/index-2.html')

def index3(request):
    return render(request, 'pricepredict/main/index-3.html')

def index6(request):
    return render(request, 'pricepredict/main/index-6.html')

def register(request):
    return render(request, 'pricepredict/main/register.html')

  # Assuming you have already created this form



# Load the trained model (ensure 'car_price_model.pkl' is in the same directory or provide the full path)
with open('pricepredict/car_price_model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Get form data
            form_data = form.cleaned_data
            # Convert form data to DataFrame
            df = pd.DataFrame([form_data])
            # Make prediction
            prediction = model.predict(df)[0]
            return render(request, 'predictor/predict.html', {'form': form, 'prediction': prediction})
    else:
        form = PredictionForm()

    return render(request, 'predictor/predict.html', {'form': form})