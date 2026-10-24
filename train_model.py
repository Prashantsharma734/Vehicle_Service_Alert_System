import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("vehicle_data.csv")

# Features
X = data[['Mileage', 'Vehicle_Age', 'Engine_Size', 'Odometer_Reading', 'Fuel_Efficiency']]

# Target
y = data['Need_Maintenance']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = RandomForestClassifier(n_estimators=100)

model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained successfully!")