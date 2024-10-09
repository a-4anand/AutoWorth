from django.shortcuts import render, redirect
import pickle
import pandas as pd
from django.shortcuts import render,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from .middlewares import auth, guest
import requests

model_path = "pricepredict/autoworthmodel.pkl"
model = pickle.load(open(model_path, 'rb'))

from django.views.decorators.csrf import csrf_exempt

# Load the dataset

# Views
@guest
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Make sure 'index' exists in your urls.py
    else:
        initial_data = {'username': '', 'password1': '', 'password2': ""}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'pricepredict/main/register.html', {'form': form})

@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        initial_data = {'username': '', 'password': ''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'pricepredict/main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')




@auth
def index(request):
    return render(request, 'pricepredict/index.html')



def index2(request):
    return render(request, 'pricepredict/main/index-2.html')



def index3(request):
    return render(request, 'pricepredict/main/index-3.html')


def register(request):
    return render(request, 'pricepredict/main/register.html')

def index6(request):
    return render(request, 'pricepredict/main/index-6.html')


# Add this import for making HTTP requests

def car_data(request):
    url = "https://car-data.p.rapidapi.com/cars"
    headers = {
        "x-rapidapi-key": "508f05fba5msh3f6c33c245b61e4p1de7abjsn6bba0f23bf58",
        "x-rapidapi-host": "car-data.p.rapidapi.com"
    }

    # Parameters for the API request
    querystring = {"limit": "10", "page": "0"}

    # Make the API request
    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        car_data = response.json()
    else:
        car_data = []
        print("Error fetching data from the car API.")

    # Render the data in a new template
    return render(request, 'car_data.html', {'car_data': car_data})


def predict_price(request):
    if request.method == 'POST':
        try:
            form_data = {
                'make': request.POST.get('make'),
                'yr_mfr': int(request.POST.get('yr_mfr')),
                'fuel_type': request.POST.get('fuel_type'),
                'kms_run': int(request.POST.get('kms_run')),
                'body_type': request.POST.get('body_type'),
                'car_rating': request.POST.get('car_rating'),
                'transmission': request.POST.get('transmission'),
                'model': request.POST.get('model'),
                'total_owners': int(request.POST.get('total_owners')),
                'registered_city': request.POST.get('registered_city'),
                'registered_state': request.POST.get('registered_state'),
                'warranty_avail': bool(request.POST.get('warranty_avail')),
                'variant': request.POST.get('variant'),
                'fitness_certificate': bool(request.POST.get('fitness_certificate')),
            }

            # Convert form data into a DataFrame to pass to the model
            input_data = pd.DataFrame([form_data])

            # Predict the price using the pre-loaded model
            predicted_price = model.predict(input_data)

            # Render the prediction result
            return render(request, 'pricepredict/main/predict_result.html', {
                'predicted_price': predicted_price[0],
                'car_details': form_data
            })

        except Exception as e:
            # Handle any exceptions during form data processing or prediction
            return HttpResponse(f"An error occurred: {str(e)}")

    # Fallback in case of a GET request or other issues
    return HttpResponse("Invalid request method.")
