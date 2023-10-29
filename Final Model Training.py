import ModelActivator as ut
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

""" PREPROCESSING: remove rows and split the data to X and y. """
preprocess = ut.DataPreprocessor()

X_data, y_data = preprocess.rmv_nans_splt_Xy(raw_and_missing_new, 'tomorrow')

"""train model on data with best hyperparameter set"""
best_params = {'max_depth': None,
               'max_features': 7,
               'min_samples_split': 20,
               'n_estimators': 50,
               'oob_score': True,
               'random_state': None}

regr = RandomForestRegressor(**best_params)

regr.fit(X_data, y_data)

"""save trained model"""
joblib.dump(regr, "./rf_compressed.joblib", compress=3)
