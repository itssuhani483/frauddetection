import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
num_records = 1000  # Total number of records
upi_ids = [f'upi_id_{i}' for i in range(1, 101)]  # 100 unique UPI IDs

# Create a synthetic dataset
data = {
    'upi_id': np.random.choice(upi_ids, num_records),
    'amount': np.random.randint(1, 50000, size=num_records),  # Transaction amounts between 1 and 50,000
    'transaction_id': [f'txn_{i}' for i in range(1, num_records + 1)],
    'timestamp': pd.date_range(start='2024-01-01', periods=num_records, freq='H'),
    'merchant': np.random.choice(['Merchant A', 'Merchant B', 'Merchant C'], num_records),
}

# Add a label for fraud detection (simple logic for demonstration)
data['is_fraud'] = (data['amount'] > 20000).astype(int)  # Mark transactions over 20,000 as fraudulent

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('synthetic_upi_transactions.csv', index=False)
print("Synthetic dataset created and saved as 'synthetic_upi_transactions.csv'")
