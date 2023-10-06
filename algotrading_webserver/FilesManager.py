import pandas as pd
from Utils import DataPreprocessor


class FilesManager:
    def __init__(self):
        self.new_day_prices = pd.DataFrame()
        self.end_of_day_prices = pd.read_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Database/end_of_day_prices.csv',
            names=['id', 'date', 'close_price'], header=None)
        self.stocks_by_id = pd.read_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Database/stocks_by_id.csv',
            names=['id', 'stock'], header=None)
        self.new_full_data = pd.DataFrame()
        self.enriched_model_input = pd.DataFrame()

    def read_input_data(self):
        self.new_day_prices = pd.read_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/model_input/latest date one stock.csv',
            index_col=0)

        """convert 'date' column to datetime data type and change its format:"""
        self.new_day_prices['date'] = pd.to_datetime(self.new_day_prices.date, dayfirst=True)
        self.new_day_prices['date'] = self.new_day_prices['date'].dt.strftime('%d/%m/%Y')

    """
    Create new csv file with updated closing prices:
    """
    def update_stocks_data(self):
        # convert 'date' column to datetime data type and change its format
        self.end_of_day_prices['date'] = pd.to_datetime(self.end_of_day_prices.date)
        self.end_of_day_prices['date'] = self.end_of_day_prices['date'].dt.strftime('%d/%m/%Y')

        merged_df = pd.merge(self.end_of_day_prices, self.new_day_prices, on=['id', 'date', 'close_price'], how='outer')
        self.new_full_data = merged_df.sort_values(['id', 'date'], key=lambda x: pd.to_datetime(x, dayfirst=True))

        # save new updated data in csv file
        self.new_full_data.to_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/model_output/new_full_data.csv', index=False)

    """
    Create 'n' features:
    """
    def prepare_for_prediction(self, num_of_days_before):
        stock_data = self.new_full_data.loc[self.new_full_data.id == 1].copy()
        preprocess = DataPreprocessor()
        raw_and_missing, missing = preprocess.add_missing_dates(stock_data, 2)
        self.enriched_model_input = pd.DataFrame(
            columns=['id', 'close_price'] + ['{}_days_ago'.format(i) for i in range(1, num_of_days_before + 1)])

        for id_value in raw_and_missing['id'].unique():
            id_df = raw_and_missing[raw_and_missing['id'] == id_value]
            close_prices = id_df['close_price'].tail(num_of_days_before + 1).values

            new_row = {'id': id_value, 'close_price': close_prices[-1]}
            for i in range(1, num_of_days_before + 1):
                new_row['{}_days_ago'.format(i)] = close_prices[-(i + 1)]

            self.enriched_model_input.loc[len(self.enriched_model_input)] = pd.Series(new_row)
