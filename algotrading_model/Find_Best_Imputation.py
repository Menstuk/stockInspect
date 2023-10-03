"""Imported libraries:"""

import Utils as ut
import pandas as pd

from tqdm import tqdm
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

"""
get stock data:
"""

stocks_by_id = pd.read_csv(
    'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Database/stocks_by_id.csv',
    names=['id',
           'stock'],
    header=None)

end_of_day_prices = pd.read_csv(
    'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Database/end_of_day_prices.csv',
    names=['id',
           'date',
           'close_price'],
    header=None)

preprocess = ut.DataPreprocessor()

activate_model = ut.ModelActivator()

"""Since stock 'BF.B' with the id of 82 is missing, we the removed it and changed ids of both tables accordingly:"""
stocks_by_id = stocks_by_id[stocks_by_id.id.isin(end_of_day_prices.id)]
stocks_by_id.drop('id', axis=1, inplace=True)
stocks_by_id['id'] = range(1, len(stocks_by_id)+1)

end_of_day_prices.loc[end_of_day_prices.id > 82, 'id'] = end_of_day_prices.loc[end_of_day_prices.id > 82, 'id']-1

"""move the position of id column:"""
cols = stocks_by_id.columns.tolist()
cols = cols[-1:] + cols[:-1]
stocks_by_id = stocks_by_id[cols]
stocks_by_id.reset_index(inplace=True)

rf_starting_params = {'n_estimators': 100, 'oob_score': True, 'random_state': 0}

imputations_dataframe = pd.DataFrame(columns=['Imputation Method', 'Dataset MSE'])

every_stock_best_imputation = pd.DataFrame(['stock name', 'Imputation Method', 'MSE'])

methods_list = [1, 2, 4]

for i in tqdm(range(1, len(stocks_by_id)+1), desc='stock'):
    stock_data = end_of_day_prices.loc[end_of_day_prices.id == i].copy()

    for method in tqdm(methods_list, desc='method'):

        """Fill each stock data with missing dates-prices by different method:
        price of the recent date/mean of prices of last 2 dates/mean of prices of last 4 dates"""
        raw_and_missing, missing = preprocess.add_missing_dates(stock_data, method)

        """Drop id column, set 'date' column as index and convert it to 'datetime' data type.
        This is done on the unified data, composed of the original dates-prices and artificially filled dates-prices"""
        # raw_and_missing data
        preprocess.alter_table(raw_and_missing, 'date', 'id')

        """create label column"""
        raw_and_missing['tomorrow'] = raw_and_missing['close_price'].shift(-1)

        """split to X and y. Remove last row (its label is nan):"""
        X, y = preprocess.rmv_nans_splt_Xy(raw_and_missing, 'tomorrow')

        """train random forest with starting parameters:"""
        regr = RandomForestRegressor(**rf_starting_params)

        regr.fit(X, y)

        y_preds = regr.predict(X)

        stock_dataset_mse = mean_squared_error(y, y_preds)

        imputations_dataframe.loc[len(imputations_dataframe)] = pd.Series({'Imputation Method': method,
                                                                           'Dataset MSE': stock_dataset_mse
                                                                           })

    best_stock_dataset_mse = imputations_dataframe['Dataset MSE'].min()

    best_row = imputations_dataframe[imputations_dataframe['Dataset MSE'] == best_stock_dataset_mse]

    every_stock_best_imputation.loc[len(every_stock_best_imputation)] = pd.Series({'stock name': (stocks_by_id[stocks_by_id['id'] == i]['stock']).iloc[0],
                                                                                   'Imputation Method': best_row['Imputation Method'],
                                                                                   'MSE': best_row['Dataset MSE']
                                                                                   })

    imputations_dataframe = pd.DataFrame(columns=['Imputation Method', 'Dataset MSE'])

print(every_stock_best_imputation)

