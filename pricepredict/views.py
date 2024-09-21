
import pickle
import pandas as pd
from django.shortcuts import render,HttpResponse
model_path = "pricepredict/autoworthmodel.pkl"
model = pickle.load(open(model_path, 'rb'))



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
    return render(request, 'pricepredict/main/index-6.html')


def fetch_news(request):
    api_key = 'e585602937ca4c43b23754b62f9276fa'
    url = f'https://newsapi.org/v2/everything?q=Indian%20Automobile&apiKey={api_key}'

    try:
        response = request.get(url)
        response.raise_for_status()
        news_data = response.json()  # Get the JSON response
        articles = news_data.get('articles', [])  # Extract the articles
    except request.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        articles = []  # If error, return empty list

    return render(request, 'pricepredict/main/index-3.html', {'articles': articles})


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
def alternative_action(request):
    if request.method == 'POST':
        # Implement the logic for the alternative action here
        return HttpResponse("Alternative action was triggered.")
    else:
        # If you want to handle GET requests, you can add that logic here
        return HttpResponse("Alternative action only supports POST requests.")