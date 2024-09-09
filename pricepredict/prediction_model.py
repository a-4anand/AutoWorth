import pandas as pd
import numpy as np
import pickle

# Load the pre-trained model from the pickle file
model_path = 'pricepredict/autoworthmodel.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

input_data = pd.read_csv('pricepredict/NewTrain.csv')
# Define a function for preprocessing the input data and making predictions
def predict_price(input_data):
    """
    Predict the car price based on input data.
    :param input_data: Dictionary containing user input from the form.
    :return: Predicted price (float)
    """
    # Example input_data dictionary:
    # input_data = {
    #     'make': 'Toyota',
    #     'yr_mfr': 2015,
    #     'fuel_type': 'Petrol',
    #     'kms_run': 40000,
    #     'body_type': 'Sedan',
    #     'car_rating': 4.5,
    #     'transmission': 'Manual',
    #     'model': 'Corolla',
    #     'total_owners': 1,
    #     'registered_city': 'Mumbai',
    #     'registered_state': 'Maharashtra',
    #     'warranty_avail': 'Yes',
    #     'variant': 'Base',
    #     'fitness_certificate': 'Valid'
    # }

    # Convert the input dictionary into a DataFrame
    input_df = pd.DataFrame([input_data])

    # Handle any necessary preprocessing here (e.g., one-hot encoding, scaling)
    # Ensure the input_df matches the format used for training the model

    # Perform prediction
    predicted_price = model.predict(input_df)

    # Return the predicted price
    return np.round(predicted_price[0], 2)
