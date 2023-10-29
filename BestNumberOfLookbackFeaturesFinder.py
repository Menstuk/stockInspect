import DataPreprocessor as Dp
import pandas as pd

from tqdm import tqdm
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

class BestNumberOfLookbackFeaturesFinder:
    def __init__(self):
        self.data_preprocessor = Dp.DataPreprocessor()
        self.days_before_list = list(range(1, 16))
        self.all_stocks_best_imputation_methods = pd.DataFrame()
        self.stock_params_df = pd.DataFrame(
            columns=['Method Number', 'Days Before', 'Train Percentage MSE', 'Test Percentage MSE'])
        self.all_stocks_best_params_df = pd.DataFrame(
            columns=['Stock Name', 'Stock Id', 'Imputation Method', 'Days Before', 'Train Percentage MSE', 'Test Percentage MSE'])

    def find_best_number_of_lookback_features(self, end_of_day_prices, stocks_by_id, rf_starting_params):

        self.all_stocks_best_imputation_methods = pd.read_csv(
            "C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/algotrading_model/parameters_evaluation/imputations_evaluations/all_stocks_best_imputation_methods.csv")

        for i in tqdm(range(1, len(stocks_by_id)+1), desc='stock'):

            stock_data = end_of_day_prices.loc[end_of_day_prices.id == i].copy()

            # fill missing dates by best method
            method_number = self.all_stocks_best_imputation_methods.loc[self.all_stocks_best_imputation_methods['Stock Id'] == i, 'Imputation Method'].iloc[0]
            raw_and_missing, missing = self.data_preprocessor.add_missing_dates(stock_data, method_number)

            # for the raw data, the unified raw and for the missing data, remove stock id column,
            # set 'date' column as index and convert 'date' column to 'datetime' data type:
            self.data_preprocessor.alter_table(stock_data, 'date', 'id')
            self.data_preprocessor.alter_table(raw_and_missing, 'date', 'id')
            self.data_preprocessor.alter_table(missing, 'date', 'id')

            for n in tqdm(self.days_before_list, desc='lookback days'):

                # create n lookback features
                raw_and_missing_new = self.data_preprocessor.create_features(raw_and_missing, n, 'close_price', '_days_ago', 'tomorrow')

                # drop all missing dates - since we want to prevent our model from learning the connections between each closing price
                raw_and_missing_new = self.data_preprocessor.drop_missing_dates(raw_and_missing_new, missing)

                ## Temporal splitting to train and test:
                split_date = self.data_preprocessor.generate_split_date(raw_and_missing_new)  # train size was set to 0.8 of data size

                train = raw_and_missing_new.iloc[raw_and_missing_new.index <= split_date].copy()
                test = raw_and_missing_new.loc[raw_and_missing_new.index > split_date].copy()

                # remove rows and split the data to X and y:
                X_train, y_train = self.data_preprocessor.rmv_nans_splt_Xy(train, 'tomorrow')
                X_test, y_test = self.data_preprocessor.rmv_nans_splt_Xy(test, 'tomorrow')

                # train random forest with starting parameters:
                regr = RandomForestRegressor(**rf_starting_params)

                regr.fit(X_train, y_train)

                y_train_preds = regr.predict(X_train)
                y_test_preds = regr.predict(X_test)

                X_train_percentage_mse = mean_squared_error(pd.array([1]).repeat(len(y_train.values)), y_train_preds / y_train.values)
                X_test_percentage_mse = mean_squared_error(pd.array([1]).repeat(len(y_test.values)), y_test_preds / y_test.values)

                self.stock_params_df.loc[len(self.stock_params_df)] = pd.Series({'Method Number': method_number,
                                                                                 'Days Before': n,
                                                                                 'Train Percentage MSE': X_train_percentage_mse,
                                                                                 'Test Percentage MSE': X_test_percentage_mse
                                                                                 })

            # calculate lowest train percentage mse
            best_lookback_mse = self.stock_params_df['Train Percentage MSE'].min()

            # get the entire row with best train percentage mse
            best_row = self.stock_params_df[self.stock_params_df['Train Percentage MSE'] == best_lookback_mse]

            self.all_stocks_best_params_df.loc[len(self.all_stocks_best_params_df)] = pd.Series({'Stock Name': (stocks_by_id[stocks_by_id['id'] == i]['stock']).iloc[0],
                                                                                                 'Stock Id': (stocks_by_id[stocks_by_id['id'] == i]['id']).iloc[0],
                                                                                                 'Imputation Method': best_row['Method Number'].iloc[0],
                                                                                                 'Days Before': best_row['Days Before'].iloc[0],
                                                                                                 'Train Percentage MSE': '{:.8f}'.format(best_row['Train Percentage MSE'].iloc[0]),
                                                                                                 'Test Percentage MSE': '{:.8f}'.format(best_row['Test Percentage MSE'].iloc[0])
                                                                                                 })

            self.stock_params_df = pd.DataFrame(
                columns=['Method Number', 'Days Before', 'Train Percentage MSE', 'Test Percentage MSE'])


        self.all_stocks_best_params_df.to_csv(
        'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/algotrading_model/parameters_evaluation/all_stocks_best_parameters.csv', index=False)
