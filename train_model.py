import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the cleaned dataset
data = pd.read_csv('cleaned_upi_transactions.csv')

# Prepare features and target variable
X = data[['upi_id', 'amount']]
y = data['is_fraud']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'upi_fraud_detection_model.pkl')
print("Model trained and saved as 'upi_fraud_detection_model.pkl'")

