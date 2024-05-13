'''
Project Title: Analysis and Visualization of Optical Signal Quality Data
File Name: analyze_data.py
Author: Jennifer Lawless

Description: Analyzes the optical signal data by creating a linear regression model
             to determine how best to predict the Q-Factor.
'''
####################################### Imports #######################################

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import sys

import parse_data

####################################### Main Program #######################################

def main(args):
    # Get username and password from the input arguments:
    USER = sys.argv[1]
    PASSWORD = sys.argv[2]

    # Call parse_data:
    optical_signal_data_list, _, _ = parse_data.main(USER, PASSWORD)

    # Print program status:
    script_name = os.path.basename(__file__)
    start_time = datetime.now()
    start_time_str = str(start_time)
    start_msg = f"********* STARTING {script_name} at {start_time_str} "
    star = "*"
    print(f"{star:*<{80}}")
    print(f"{start_msg:*<{80}}\n")
    print("Now building the Linear Regression model........\n")

    # Initialize an empty list to hold DataFrames:
    df_list = []

    # Loop through the data and append it to the DataFrame:
    for lab in optical_signal_data_list:
        for data_timestamp in lab.timestamp_list:
            for node_data in data_timestamp.node_data_list:
                current_metrics = {
                    'timestamp': data_timestamp.timestamp,
                    'power': node_data.measurements.instantaneous.power,
                    'ber': node_data.measurements.instantaneous.ber,
                    'snr': node_data.measurements.instantaneous.snr,
                    'dgd': node_data.measurements.instantaneous.dgd,
                    'qfactor': node_data.measurements.instantaneous.qfactor,
                    'chromatic_dispersion': node_data.measurements.instantaneous.chromatic_dispersion,
                    'carrier_offset': node_data.measurements.instantaneous.carrier_offset,
                }
                df_list.append(pd.DataFrame(current_metrics, index=[0]))

    # Concatenate all the DataFrames in the list:
    df = pd.concat(df_list, ignore_index=True)

    # Define the feature columns:
    feature_cols = ['power', 'ber', 'snr', 'dgd', 'chromatic_dispersion', 'carrier_offset']

    # Create the features (X) and target (y) sets:
    X = df[feature_cols]
    y = df['qfactor']

    # Combine X and y into a single DataFrame:
    df_combined = pd.concat([X, y], axis=1)

    # Drop any missing or NaN values:
    df_combined = df_combined.dropna()

    # Print the correlation of each feature with the target variable
    print("Correlation with Q-factor:")
    correlation_matrix = df_combined.corr()
    print(correlation_matrix['qfactor'])
    print()

    # Select features with correlation > 0.3:
    selected_features = [feature for feature in feature_cols if abs(correlation_matrix.loc[feature, 'qfactor']) > 0.3]
    print(f"Selected features based on correlation: {selected_features}")

    # Split the data into training and test sets:
    X_train, X_test, y_train, y_test = train_test_split(X[selected_features], y, test_size=0.2, random_state=42)

    # Fit the model on the training data with the selected features:
    model = sm.OLS(y_train, sm.add_constant(X_train))
    results = model.fit()

    # Make predictions on the test data with the selected features:
    y_pred = results.predict(sm.add_constant(X_test))

    # Calculate and output the mean squared error of the predictions with the selected features:
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error with selected features: {mse}")

    # Plot the actual vs predicted values:
    plt.figure(figsize=(10,6))
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs Predicted Q-Factor')
    plt.show()

    # Print program status:
    end_time = datetime.now()
    end_time_str = str(end_time)
    elapsed_time = end_time - start_time
    elapsed_time_str = str(elapsed_time)
    end_msg = f"\n********* ENDING {script_name} at {end_time_str} "
    elapsed_time_msg = f"\n********* Elapsed Time: {elapsed_time_str} "
    print(f"{end_msg:*<{80}}")
    print(f"{elapsed_time_msg:*<{80}}")
    print(f"{star:*<{80}}")


if __name__ == "__main__":
    main(sys.argv[1:])
