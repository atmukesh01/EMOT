# File: 03_train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import joblib

def train_model(X_train_path='X_train.csv', y_train_path='y_train.csv'):
    """
    Loads training data, performs hyperparameter tuning using GridSearchCV,
    and saves the best model.
    """
    # Load training data
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).squeeze() # Use squeeze to make it a Series
    print("Training data loaded.")

    # Define the model
    rf = RandomForestRegressor(random_state=42)

    # Define the hyperparameter grid for GridSearchCV
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }

    # Set up GridSearchCV
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        verbose=2
    )

    # Fit the model
    print("Starting model training and hyperparameter tuning...")
    grid_search.fit(X_train, y_train)

    # Get the best model
    best_model = grid_search.best_estimator_
    print(f"Best parameters found: {grid_search.best_params_}")

    # Save the final model
    joblib.dump(best_model, 'final_model.pkl')
    print("Final model saved as 'final_model.pkl'")

if __name__ == '__main__':
    train_model()