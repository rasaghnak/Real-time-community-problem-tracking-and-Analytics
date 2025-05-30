import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Function to generate random patient data
def generate_patient_data(num_records=10):
    patient_ids = [f"P{str(i).zfill(3)}" for i in range(1, num_records+1)]
    names = ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Brown', 'Eve Davis', 'Quinn Johnson', 'Rachel Lee', 'Samuel Adams', 'Tiffany Scott', 'Uriel Brown']
    ages = np.random.randint(20, 80, size=num_records)
    genders = np.random.choice(['M', 'F'], size=num_records)
    addresses = [f"{i} Elm St" for i in range(1, num_records+1)]
    contact_numbers = [f"555-{str(np.random.randint(1000, 9999))}" for _ in range(num_records)]
    admission_dates = [(datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d') for _ in range(num_records)]
    diagnosis_codes = np.random.choice(['D001', 'D002', 'D003', 'D004', 'D005'], size=num_records)

    return pd.DataFrame({
        'patient_id': patient_ids,
        'name': names[:num_records],
        'age': ages,
        'gender': genders,
        'address': addresses,
        'contact_number': contact_numbers,
        'admission_date': admission_dates,
        'diagnosis_code': diagnosis_codes
    })

# Generate Data
data = generate_patient_data()

# Save data to local CSV
local_file_path = "/tmp/raw_patients_daily.csv"
data.to_csv(local_file_path, index=False)

# Upload the file to DBFS
dbfs_file_path = f"dbfs:/FileStore/healthcare/raw_data/patients_data_{datetime.now().strftime('%Y%m%d%H%M')}.csv"

# Using dbutils to put file into DBFS
dbutils.fs.cp(f"file://{local_file_path}", dbfs_file_path)

print(f"Data saved to {dbfs_file_path}")