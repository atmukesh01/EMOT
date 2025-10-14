import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import os

def train_model(X_train_path='X_train_enhanced.csv', y_train_path='y_train_enhanced.csv'):
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).squeeze()
    
    rf = RandomForestRegressor(random_state=42)
    param_grid = { 'n_estimators': [100, 200], 'max_depth': [10, 20, 30], 'min_samples_split': [2, 5] }
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    
    # Save the model inside the 'predictor' app directory
    output_path = os.path.join('predictor', 'final_model_enhanced.pkl')
    joblib.dump(best_model, output_path)
    print(f"Enhanced model saved to: {output_path}")

if __name__ == '__main__':
    train_model()