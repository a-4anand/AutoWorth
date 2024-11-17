import json
from .middlewares import auth, guest
from django.conf import settings
from django.http import JsonResponse
import random
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

import pickle
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
import pickle
from .models import BikeListing
from .forms import BikeListingForm



from django.shortcuts import render, redirect, get_object_or_404
from .models import VehicleListing, UserInterest
from .forms import VehicleListingForm

# views.py


model_path = "pricepredict/autoworthmodel.pkl"
model = pickle.load(open(model_path, 'rb'))

def generate_otp():
    return str(random.randint(100000, 999999))

# Helper function to send OTP email
def send_otp_email(email, otp):
    subject = "Your OTP for AutoWorth Registration"
    message = f"Your OTP is: {otp}. Please enter this code to complete your registration."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# Views

@guest
 # Assuming this is your OTP sending utility

def register_view(request):
    if request.method == 'POST':
        # Get data from the registration form
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email:
            return render(request, 'pricepredict/main/register.html', {
                "error": "Email is required"
            })

        # Generate OTP and send it via email
        otp = random.randint(100000, 999999)
        send_otp_email(email, otp)

        # Store the OTP and email in the session
        request.session['otp'] = otp
        request.session['email'] = email
        request.session['username'] = username
        request.session['password1'] = password1
        request.session['password2'] = password2

        # Redirect to OTP verification page
        return redirect('otp_verify')

    # Initial form load for GET request
    form = UserCreationForm()
    return render(request, 'pricepredict/main/register.html', {
        "form": form
    })

@guest
def otp_verify_view(request):
    if request.method == 'POST':
        # Get OTP entered by the user
        otp_entered = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if not otp_entered:
            return render(request, 'pricepredict/main/otp_verify.html', {
                "error": "OTP is required"
            })

        # Validate OTP
        if otp_entered != str(stored_otp):
            return render(request, 'pricepredict/main/otp_verify.html', {
                "error": "Invalid OTP. Please try again."
            })

        # OTP is correct, so create the user
        email = request.session.get('email')
        username = request.session.get('username')
        password1 = request.session.get('password1')
        password2 = request.session.get('password2')

        # Create the user
        form = UserCreationForm({
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2
        })

        if form.is_valid():
            user = form.save()
            login(request, user)

            # Clear OTP and session data
            request.session.pop('otp', None)
            request.session.pop('email', None)
            request.session.pop('username', None)
            request.session.pop('password1', None)
            request.session.pop('password2', None)

            return redirect('index')  # Redirect to home page or dashboard

        return render(request, 'pricepredict/main/otp_verify.html', {
            "error": "There was an issue with your registration."
        })

    # Show OTP form
    return render(request, 'pricepredict/main/otp_verify.html')
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


# @auth
# def index2(request):
#     return render(request, 'pricepredict/main/index-2.html')


@auth
def index3(request):
    return render(request, 'pricepredict/main/index-3.html')

@auth
def register(request):
    return render(request, 'pricepredict/main/register.html')
@auth
def index6(request):
    return render(request, 'pricepredict/main/index-6.html')


# Add this import for making HTTP requests



@auth
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








@auth
def create_listing(request):
    if request.method == 'POST':
        form = VehicleListingForm(request.POST, request.FILES)  # Ensure request.FILES is used for file uploads
        if form.is_valid():
            car_listing = form.save(commit=False)
            car_listing.owner = request.user
            car_listing.save()
            return redirect('view_listings')
        else:
            print(form.errors)  # This will print form errors to the console
    else:
        form = VehicleListingForm()
    return render(request, 'pricepredict/main/add_listing.html', {'form': form})
@auth
def express_interest(request, listing_id):
    car_listing = get_object_or_404(VehicleListing, id=listing_id)
    if request.method == 'POST':
        message = request.POST['message']
        UserInterest.objects.create(user=request.user, car_listing=car_listing, message=message)
        return redirect('view_listings')
    return render(request, 'pricepredict/main/express_interest.html', {'car_listing': car_listing})

@auth

def bike_listings(request):
    return render(request, 'pricepredict/main/bike-listing.html')

@auth
def view_listings(request):
    listings = VehicleListing.objects.all()  # Retrieves all vehicle listings from the database
    return render(request, 'pricepredict/main/view_listing.html', {'vehicle_list': listings})


from django.http import HttpResponseForbidden


@auth
def delete_listing(request, listing_id):
    car_listing = get_object_or_404(VehicleListing, id=listing_id)

    # Check if the logged-in user is the owner of the listing
    if car_listing.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this listing.")

    if request.method == 'POST':
        car_listing.delete()  # Delete the listing
        return redirect('view_listings')  # Redirect to the listings page after deletion

    return render(request, 'pricepredict/main/delete_listing.html', {'car_listing': car_listing})


from django.core.mail import send_mail
from django.http import HttpResponse


def send_test_email(request):
    subject = 'Test Email'
    message = 'This is a test to ensure your email settings work.'
    from_email = 'AutoWorth Support <ad3810242@gmail.com>'
    recipient_list = ['anand.dubey@msds.christuniversity.in']  # Replace with your own email

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return HttpResponse('Test email sent successfully.')
    except Exception as e:
        return HttpResponse(f'Error sending email: {str(e)}')








from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import VehicleListing  # Ensure this is your car listing model


def express_interest(request, listing_id):
    # Retrieve car listing based on listing_id
    car_listing = get_object_or_404(VehicleListing, id=listing_id)

    if request.method == "POST":
        # Check if the user is authenticated before accessing user information
        if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to express interest in this car.")

        # Get the message from the form (empty string if not provided)
        message = request.POST.get("message", "").strip()

        # If no message is provided, you can either raise an error or proceed without it
        if not message:
            return HttpResponse("Please provide a message expressing your interest.")

        # Prepare email details
        subject = f"Interest in Car Listing: {car_listing.make} {car_listing.model}"
        from_email = "AutoWorth Support <ad3810242@gmail.com>"  # Sender email address
        recipient_list = ["ad3810242@gmail.com"]  # Your email address

        # Compose email message
        email_message = f"""
        Hello,

        {request.user.username} has expressed interest in the {car_listing.make} {car_listing.model} listed by {car_listing.owner} on AutoWorth. 
        Please contact the owner at {car_listing.phone_no}.

        Message from the user:
        {message}

        Best regards,
        AutoWorth Team
        """

        try:
            # Send the email
            send_mail(subject, email_message, from_email, recipient_list, fail_silently=False)
            return HttpResponse("Thank you! Your interest has been submitted.")
        except Exception as e:
            return HttpResponse(f"There was an error sending your interest. Please try again later. Error: {str(e)}")

    # Render the page if the request method is GET or the form is not submitted
    return render(request, "pricepredict/main/express_interest.html", {"car_listing": car_listing})



# added for bike price prediction by anand dubey @ 9 nov 2024
import numpy as np
import joblib
from django.shortcuts import render
from .forms import BikePriceForm

# Load the model and encoders once at the top of the file
model1 = joblib.load('models/bike_price_model.pkl')
le_bike_name = joblib.load('models/le_bike_name.pkl')
le_city = joblib.load('models/le_city.pkl')
le_owner = joblib.load('models/le_owner.pkl')
le_brand = joblib.load('models/le_brand.pkl')

def predict_bike_price(request):
    result = None

    if request.method == 'POST':
        form = BikePriceForm(request.POST)
        if form.is_valid():
            # Get data from the form
            bike_name = form.cleaned_data['bike_name']
            city = form.cleaned_data['city']
            kms_driven = form.cleaned_data['kms_driven']
            owner = form.cleaned_data['owner']
            age = form.cleaned_data['age']
            power = form.cleaned_data['power']
            brand = form.cleaned_data['brand']

            # Encode inputs
            bike_name_encoded = le_bike_name.transform([bike_name])[0] if bike_name in le_bike_name.classes_ else -1
            city_encoded = le_city.transform([city])[0] if city in le_city.classes_ else -1
            owner_encoded = le_owner.transform([owner])[0] if owner in le_owner.classes_ else -1
            brand_encoded = le_brand.transform([brand])[0] if brand in le_brand.classes_ else -1

            # Handle unknown categories
            if -1 in (bike_name_encoded, city_encoded, owner_encoded, brand_encoded):
                result = "Error: Some input values are not recognized. Please check your input."
            else:
                # Prepare data for prediction
                input_data = np.array([[bike_name_encoded, city_encoded, kms_driven, owner_encoded, age, power, brand_encoded]])
                predicted_price = model1.predict(input_data)
                result = f"The predicted price of the bike is: {predicted_price[0]:.2f}"
    else:
        form = BikePriceForm()

    return render(request, 'pricepredict/main/predict_bike_price.html', {'form': form, 'result': result})


# bike marketplace



@auth

def bike_listing(request):
    vehicles = BikeListing.objects.all()  # Fetch all bike listings
    return render(request, 'pricepredict/main/bike-listing.html', {'vehicle_list': vehicles})

#
#
def add_bike(request):
    if request.method == 'POST':
        form = BikeListingForm(request.POST, request.FILES)
        if form.is_valid():
            bike_listing = form.save(commit=False)
            bike_listing.owner = request.user
            bike_listing.save()
            # Save the new listing with the owner being the current logged-in user
            form.save()
            return redirect('bike_listing')
    else:
        form = BikeListingForm()
    return render(request, 'pricepredict/main/add_bike.html', {'form': form})

def delete_bike(request, listing_id):
    bike_listing = get_object_or_404(BikeListing, id=listing_id)

    # Ensure only the owner can delete the listing
    if bike_listing.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this listing.")

    if request.method == 'POST':
        bike_listing.delete()  # Delete the listing
        return redirect('bike_listing')  # Redirect after deletion

    return render(request, 'pricepredict/main/delete_listing.html', {'bike_listing': bike_listing})


def express_interest_bike(request, listing_id):
    # Retrieve car listing based on listing_id
    bike_listing = get_object_or_404(BikeListing, id=listing_id)

    if request.method == "POST":
        # Check if the user is authenticated before accessing user information
        if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to express interest in this car.")

        # Get the message from the form (empty string if not provided)
        message = request.POST.get("message", "").strip()

        # If no message is provided, you can either raise an error or proceed without it
        if not message:
            return HttpResponse("Please provide a message expressing your interest.")

        # Prepare email details
        subject = f"Interest in Car Listing: {bike_listing.company} {bike_listing.model}"
        from_email = "AutoWorth Support <ad3810242@gmail.com>"  # Sender email address
        recipient_list = ["ad3810242@gmail.com"]  # Your email address

        # Compose email message
        email_message = f"""
        Hello,

        {request.user.username} has expressed interest in the {bike_listing.company} {bike_listing.model} listed by {bike_listing.owner} on AutoWorth. 
        Please contact the owner at {bike_listing.phone_no}.

        Message from the user:
        {message}

        Best regards,
        AutoWorth Team
        """

        try:
            # Send the email
            send_mail(subject, email_message, from_email, recipient_list, fail_silently=False)
            return HttpResponse("Thank you! Your interest has been submitted.")
        except Exception as e:
            return HttpResponse(f"There was an error sending your interest. Please try again later. Error: {str(e)}")

    # Render the page if the request method is GET or the form is not submitted
    return render(request, "pricepredict/main/express_interest_bike.html", {"bike_listing": bike_listing})