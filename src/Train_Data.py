# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import permutation_importance
import joblib

# Step 1: Load the dataset with the correct delimiter
data = pd.read_csv('data_stress-2.csv', sep=';')

# Step 2: Clean column names by stripping whitespace
data.columns = data.columns.str.strip()

# Step 3: Replace commas with dots and convert to numeric
for column in data.columns[:-1]:
    data[column] = data[column].str.replace(',', '.').astype(float)

# Step 4: Ensure the target variable is numeric
data['Stress Levels'] = data['Stress Levels'].astype(int)

# Step 5: Check for missing values
print("Missing values in the dataset:\n", data.isnull().sum())

# Step 6: Handling Missing Values
# Create binary features indicating missing values
for column in ['body temperature', 'limb movement', 'blood oxygen',
               'eye movement', 'hours of sleep', 'heart rate']:
    data[f'{column}_missing'] = data[column].isnull().astype(int)

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
data.iloc[:, :-1] = imputer.fit_transform(data.iloc[:, :-1])  # Imputing only feature columns

# Step 7: Select features and target labels
X = data[['snoring range', 'respiration rate', 'body temperature', 'limb movement',
           'blood oxygen', 'eye movement', 'hours of sleep', 'heart rate'] +
           [f'{column}_missing' for column in ['body temperature', 'limb movement',
                                                'blood oxygen', 'eye movement',
                                                'hours of sleep', 'heart rate']]]
y = data['Stress Levels']

# Step 8: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 9: Normalize the feature data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 10: Apply SMOTE to handle class imbalance
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Step 11: Create and train the MLPClassifier model
model = MLPClassifier(max_iter=1000, random_state=42, early_stopping=True, validation_fraction=0.2)

# Step 12: Define hyperparameters to tune
param_grid = {
    'hidden_layer_sizes': [(10, 10), (20, 10), (20, 20)],
    'activation': ['tanh', 'relu'],
    'solver': ['sgd', 'adam'],
    'alpha': [0.0001, 0.001, 0.01],
    'learning_rate': ['constant', 'adaptive'],
}

# Step 13: Perform GridSearchCV to find the best model
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train_balanced, y_train_balanced)

# Step 14: Get the best model from GridSearchCV
best_model = grid_search.best_estimator_
print("Best Hyperparameters:", grid_search.best_params_)

# Step 15: Evaluate the best model using cross-validation
cv_scores = cross_val_score(best_model, X_train_balanced, y_train_balanced, cv=5)
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Average Cross-Validation Score: {np.mean(cv_scores)}")

# Step 16: Train the best model on the balanced training data
best_model.fit(X_train_balanced, y_train_balanced)

# Step 17: Make predictions on the test data
y_pred = best_model.predict(X_test)

# Step 18: Evaluate the model with a confusion matrix and classification report
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Step 19: Visualize the confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
            xticklabels=np.unique(y), yticklabels=np.unique(y))
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.show()

# Step 20: Plot the training loss curve
plt.plot(best_model.loss_curve_)
plt.title('Model Training Loss Curve')
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.show()

# Step 21: Feature Importance using Permutation Importance
result = permutation_importance(best_model, X_test, y_test, n_repeats=30, random_state=42)
sorted_idx = result.importances_mean.argsort()

# Step 22: Plot Feature Importance
plt.figure(figsize=(10, 6))
plt.barh(range(len(sorted_idx)), result.importances_mean[sorted_idx], align='center')
plt.yticks(range(len(sorted_idx)), np.array(X.columns)[sorted_idx])
plt.title('Feature Importance')
plt.xlabel('Permutation Importance')
plt.show()

# Save the best model to a file
import os

# Save the best model to a file
joblib.dump(best_model, '../data/best_stress_model.pkl')

# Check if the file has been created
if os.path.exists('best_stress_model.pkl'):
    print("Model file 'best_stress_model.pkl' created successfully.")
else:
    print("Model file 'best_stress_model.pkl' was not created.")

