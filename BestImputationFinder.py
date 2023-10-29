import DataPreprocessor as Dp
import pandas as pd

from tqdm import tqdm
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor


class BestImputationFinder:
    def __init__(self):
        self.data_preprocessor = Dp.DataPreprocessor()
        self.imputations_dataframe = pd.DataFrame(columns=['Imputation Method', 'Dataset Percentage MSE'])
        self.every_stock_best_imputation = pd.DataFrame(columns=['Stock Name', 'Stock Id', 'Imputation Method', 'Percentage MSE'])
        self.methods_list = [1, 2, 4]

    def find_best_imputation(self, end_of_day_prices, stocks_by_id, rf_starting_params):

        for i in tqdm(range(1, len(stocks_by_id)+1), desc='stock'):

            stock_data = end_of_day_prices.loc[end_of_day_prices.id == i].copy()

            for method in tqdm(self.methods_list, desc='method'):

                """Fill each stock data with missing dates-prices by different method:
                price of the recent date/mean of prices of last 2 dates/mean of prices of last 4 dates"""
                raw_and_missing, missing = self.data_preprocessor.add_missing_dates(stock_data, method)

                """Drop id column, set 'date' column as index and convert it to 'datetime' data type.
                This is done on the unified data, composed of the original dates-prices and artificially filled dates-prices"""
                # raw_and_missing data
                self.data_preprocessor.alter_table(raw_and_missing, 'date', 'id')

                """create label column"""
                raw_and_missing['tomorrow'] = raw_and_missing['close_price'].shift(-1)

                """split to X and y. Remove last row (its label is nan):"""
                X, y = self.data_preprocessor.rmv_nans_splt_Xy(raw_and_missing, 'tomorrow')

                """train random forest with starting parameters:"""
                regr = RandomForestRegressor(**rf_starting_params)

                regr.fit(X, y)

                y_preds = regr.predict(X)

                stock_dataset_mse = mean_squared_error(pd.array([1]).repeat(len(y.values)), y_preds / y.values)

                self.imputations_dataframe.loc[len(self.imputations_dataframe)] = pd.Series({'Imputation Method': method,
                                                                                             'Dataset Percentage MSE': stock_dataset_mse
                                                                                             })

            best_stock_dataset_mse = self.imputations_dataframe['Dataset Percentage MSE'].min()

            best_row = self.imputations_dataframe[self.imputations_dataframe['Dataset Percentage MSE'] == best_stock_dataset_mse]

            self.every_stock_best_imputation.loc[len(self.every_stock_best_imputation)] = pd.Series({
                'Stock Name': (stocks_by_id[stocks_by_id['id'] == i]['stock']).iloc[0],
                'Stock Id': (stocks_by_id[stocks_by_id['id'] == i]['id']).iloc[0],
                'Imputation Method': best_row['Imputation Method'].iloc[0],
                'Percentage MSE': '{:.8f}'.format(best_row['Dataset Percentage MSE'].iloc[0])
            })

            self.imputations_dataframe = pd.DataFrame(columns=['Imputation Method', 'Dataset Percentage MSE'])

        path = "C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/algotrading_model/parameters_evaluation/imputations_evaluations/all_stocks_best_imputation_methods.csv"
        self.every_stock_best_imputation.to_csv(path, index=False)

