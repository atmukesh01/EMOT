# File: 03_train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import joblib

def train_model(X_train_path='X_train_enhanced.csv', y_train_path='y_train_enhanced.csv'):
    """
    Loads enhanced training data, performs hyperparameter tuning,
    and saves the best model.
    """
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).squeeze()
    print("Enhanced training data loaded.")

    rf = RandomForestRegressor(random_state=42)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    
    grid_search = GridSearchCV(
        estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2
    )

    print("Starting model training with enhanced data...")
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print(f"Best parameters found: {grid_search.best_params_}")

    joblib.dump(best_model, 'final_model_enhanced.pkl')
    print("Enhanced model saved as 'final_model_enhanced.pkl'")

if __name__ == '__main__':
    train_model()