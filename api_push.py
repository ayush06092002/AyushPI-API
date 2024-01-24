import pandas as pd
import requests
import json
import sys

# Replace with your API endpoint and token
api_url = "http://localhost:8000/api/medicine/medicines/"
headers = {
    "Authorization": "Token 2fb6ba6a7c929c54cdc667995b2daf546c9f2e8b",
    "Content-Type": "application/json",
}

# Read the Excel file
excel_file = "final_data.xlsx"
df = pd.read_excel(excel_file, header=None)  # Assuming no header in the Excel file

# Initialize variables to track medicine and symptoms
current_medicine = ""
medicine_data = {}  # Dictionary to store data for each medicine

# Iterate through rows in the Excel file
for index, row in df.iterrows():
    try:
        # Extract data based on index
        name = row[0]
        ref_text = row[1]
        dispensing_size = row[2]
        dosage = row[3]
        precautions = row[4]
        preferred_use = row[5]
        symptom = row[6]

        # Check if the medicine name has changed
        if name != current_medicine:
            # If the current medicine is different, create a new medicine_data dictionary
            medicine_data[name] = {
                "name": name,
                "ref_text": ref_text,
                "dispensing_size": dispensing_size,
                "dosage": dosage,
                "precautions": precautions,
                "preferred_use": preferred_use,
                "symptoms": [],  # Initialize an empty symptoms list
            }
            current_medicine = name

        # Append symptom to the symptoms list of the current medicine
        medicine_data[name]["symptoms"].append({"name": symptom})

    except Exception as e:
        print(f"Error processing row {index}: {str(e)}")
        print(f"Problematic values: {json.dumps(row.values.tolist())}")

# Iterate through medicine_data and send POST requests for each medicine
for medicine_name, data in medicine_data.items():
    try:
        # Send the POST request for each medicine's data
        response = requests.post(api_url, json=data, headers=headers)

        # Check for successful response
        if response.status_code == 201:  # Assuming 201 is the status code for a successful POST request
            print(f"Successfully posted data for {medicine_name}")
        else:
            print(f"Failed to post data for {medicine_name}")
            print(f"Error response for {medicine_name}: {response.status_code}")
            print(f"Error message: {response.text}")

    except Exception as e:
        print(f"Error processing medicine {medicine_name}: {str(e)}")

print("All data processed")
