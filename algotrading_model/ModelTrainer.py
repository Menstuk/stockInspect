import DataPreprocessor as Dp
import pandas as pd
import joblib

from tqdm import tqdm
from sklearn.ensemble import RandomForestRegressor


class ModelTrainer:
    def __init__(self):
        self.new_full_data = pd.DataFrame()
        self.all_stocks_best_parameters = pd.DataFrame()
        self.data_preprocessor = Dp.DataPreprocessor()

    def train_models(self, rf_starting_params):

        self.all_stocks_best_parameters = pd.read_csv(
            "C:/Users/manor/Desktop/Final Project - Algotrading\First Developement Step/algotrading_model/parameters_evaluation/all_stocks_best_parameters.csv")

        self.new_full_data = pd.read_csv(
            "C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/read_input_data/new_full_data.csv")

        stocks_by_id = self.all_stocks_best_parameters[['Stock Name', 'Stock Id']]

        imputation_methods = self.all_stocks_best_parameters[['Stock Id', 'Imputation Method']]

        days_before = self.all_stocks_best_parameters[['Stock Id', 'Days Before']]

        for i in tqdm(range(1, len(stocks_by_id)+1), desc='stock'):

            stock_data = self.new_full_data.loc[self.new_full_data.id == i].copy()

            # fill missing dates by best method
            method_number = imputation_methods.loc[imputation_methods['Stock Id'] == i, 'Imputation Method'].iloc[0]
            raw_and_missing, missing = self.data_preprocessor.add_missing_dates(stock_data, method_number)

            # for the raw data, the unified raw and for the missing data, remove stock id column,
            # set 'date' column as index and convert 'date' column to 'datetime' data type:
            self.data_preprocessor.alter_table(stock_data, 'date', 'id')
            self.data_preprocessor.alter_table(raw_and_missing, 'date', 'id')
            self.data_preprocessor.alter_table(missing, 'date', 'id')

            # create n lookback features
            n = int(days_before.loc[days_before['Stock Id'] == i, 'Days Before'].iloc[0])
            raw_and_missing_new = self.data_preprocessor.create_features(raw_and_missing, n, 'close_price', '_days_ago', 'tomorrow')

            # drop all missing dates - since we want to prevent our model from learning the connections between each closing price
            raw_and_missing_new = self.data_preprocessor.drop_missing_dates(raw_and_missing_new, missing)

            # remove rows and split the data to X and y:
            X_data, y_data = self.data_preprocessor.rmv_nans_splt_Xy(raw_and_missing_new, 'tomorrow')

            # train random forest with starting parameters:
            regr = RandomForestRegressor(**rf_starting_params)

            regr.fit(X_data, y_data)

            """save trained models"""
            joblib.dump(regr, f'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/algotrading_model/rf_models/rf_for_stock_{i}_compressed.joblib', compress=3)



