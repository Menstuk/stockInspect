import pandas as pd


class FilesManager:
    def __init__(self):
        self.new_day_prices = pd.DataFrame()
        self.new_day_prices_ids = []
        # self.new_full_data = pd.read_csv('C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/read_input_data/new_full_data.csv')
        self.new_full_data = pd.read_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/read_input_data/new_full_data_test.csv')
        self.stocks_by_id = pd.read_csv('C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/read_input_data/stocks_by_id_after_editing.csv')
        self.all_stocks_best_parameters = pd.read_csv(
            "C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/algotrading_model/parameters_evaluation/all_stocks_best_parameters.csv")
        self.stock_id_to_days_before = {}
        self.enriched_model_input = pd.DataFrame(
            columns=['id', 'close_price'] + ['{}_days_ago'.format(i) for i in range(1, 16)])

    def read_input_data(self):
        self.new_day_prices = pd.read_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/read_input_data/model_input/latest dates of stocks.csv',
            index_col=0)

        """convert 'date' column to datetime data type and change its format:"""
        self.new_day_prices['date'] = pd.to_datetime(self.new_day_prices.date, dayfirst=True)
        self.new_day_prices['date'] = self.new_day_prices['date'].dt.strftime('%d/%m/%Y')

    """
    Create new csv file with updated closing prices:
    """
    def update_stocks_data(self):
        # convert 'date' column to datetime data type and change its format
        self.new_full_data['date'] = pd.to_datetime(self.new_full_data.date, dayfirst=True)
        self.new_full_data['date'] = self.new_full_data['date'].dt.strftime('%d/%m/%Y')

        # convert 'close_price' column to float data type
        self.new_day_prices['close_price'] = self.new_day_prices['close_price'].astype(float)

        merged_df = pd.merge(self.new_full_data, self.new_day_prices, on=['id', 'date', 'close_price'], how='outer')
        self.new_full_data = merged_df.sort_values(['id', 'date'], key=lambda x: pd.to_datetime(x, dayfirst=True))

        self.new_day_prices_ids = self.new_day_prices["id"].tolist()

        # save new updated data in csv file
        # self.new_full_data.to_csv(
        #     "C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/read_input_data/new_full_data.csv", index=False)
        self.new_full_data.to_csv(
            "C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/read_input_data/new_full_data_test.csv",
            index=False)
        print(f'Ids Of New Stock Data: {self.new_day_prices["id"].tolist()}')
        print(f'Date Of New Stock Data: {self.new_day_prices["date"].iloc[0]}')

    """
    Create 'n' features:
    """
    def prepare_for_prediction(self, data_preprocessor):
        for stock_id in self.new_day_prices_ids:
            stock_data = self.new_full_data.loc[self.new_full_data.id == stock_id].copy()

            # fill missing dates by best method
            method_number = self.all_stocks_best_parameters.loc[self.all_stocks_best_parameters['Stock Id'] == stock_id, 'Imputation Method'].iloc[0]
            raw_and_missing, missing = data_preprocessor.add_missing_dates(stock_data, method_number)

            num_of_days_before = int(self.all_stocks_best_parameters.loc[self.all_stocks_best_parameters['Stock Id'] == stock_id, 'Days Before'].iloc[0])
            self.stock_id_to_days_before[stock_id] = num_of_days_before

            for id_value in raw_and_missing['id'].unique():
                id_df = raw_and_missing[raw_and_missing['id'] == id_value]
                close_prices = id_df['close_price'].tail(num_of_days_before + 1).values

                new_row = {'id': id_value, 'close_price': close_prices[-1]}
                for i in range(1, num_of_days_before + 1):
                    new_row['{}_days_ago'.format(i)] = close_prices[-(i + 1)]

                self.enriched_model_input.loc[len(self.enriched_model_input)] = pd.Series(new_row)

    def get_paths_by_ids(self):
        paths_list = [
            f'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/algotrading_model/rf_models/rf_for_stock_{stock_id}_compressed.joblib'
            for stock_id in self.new_day_prices_ids
                    ]
        return paths_list
