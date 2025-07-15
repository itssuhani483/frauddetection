import pandas as pd

# Load the dataset
data = pd.read_csv('synthetic_upi_transactions.csv')

# Check for missing values
print(data.isnull().sum())

# Remove duplicates if any
data.drop_duplicates(inplace=True)

# Encode categorical features
data['upi_id'] = data['upi_id'].astype('category').cat.codes  # Convert UPI IDs to numerical values

# Save the cleaned data
data.to_csv('cleaned_upi_transactions.csv', index=False)
print("Data cleaned and saved as 'cleaned_upi_transactions.csv'")
