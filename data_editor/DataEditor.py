import pandas as pd


class DataEditor:

    def __init__(self):
        self.stocks_by_id = pd.read_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Database/stocks_by_id.csv',
            names=['id', 'stock'], header=None)
        self.end_of_day_prices = pd.read_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Database/end_of_day_prices.csv',
            names=['id', 'date', 'close_price'], header=None)
        self.missing_id = 0

    def convert_data_columns(self):
        """convert 'date' column to datetime data type and change its format:"""
        self.end_of_day_prices['date'] = pd.to_datetime(self.end_of_day_prices.date)
        self.end_of_day_prices['date'] = self.end_of_day_prices['date'].dt.strftime('%d/%m/%Y')

    def get_missing_stock_ids(self):
        common = self.stocks_by_id[['id']].merge(self.end_of_day_prices['id'].drop_duplicates(), how='left', indicator=True)
        self.missing_id = common[common['_merge'] == 'left_only']['id'].iloc[0]

    """Stock 'BF.B' with the id of 82 is missing.
    Stock 'BRK.B' with the id of 66 has only 14 and is the only stock to have 27/09/2017 as its latest date.   
    Therefore, we removed them and changed ids of both tables accordingly:"""
    def remove_stocks_by_id(self):

        #remove the missing stock from stocks_by_id
        self.stocks_by_id = self.stocks_by_id[self.stocks_by_id.id.isin(self.end_of_day_prices.id)]

        #remove sparse stock from stocks_by_id and reindex
        self.stocks_by_id = self.stocks_by_id[self.stocks_by_id['id'] != 66]
        self.stocks_by_id = self.stocks_by_id.iloc[:, self.stocks_by_id.columns != 'id']
        self.stocks_by_id['id'] = range(1, len(self.stocks_by_id) + 1)

        # remove sparse stock from end_of_day_prices and reindex
        self.end_of_day_prices = self.end_of_day_prices.loc[self.end_of_day_prices.id != 66]
        self.end_of_day_prices.loc[(self.end_of_day_prices['id'] > 66) & (self.end_of_day_prices.id < self.missing_id), 'id'] -= 1
        self.end_of_day_prices.loc[self.end_of_day_prices.id > self.missing_id, 'id'] -= 2

        """move the position of id column:"""
        cols = self.stocks_by_id.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        self.stocks_by_id = self.stocks_by_id[cols]
        self.stocks_by_id = self.stocks_by_id.reset_index()

        """create csv files containing updated data - without missing stocks"""
        self.end_of_day_prices.to_csv("C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Edited Databases/end_of_day_prices_after_editing.csv", index=False)
        self.stocks_by_id.to_csv("C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Edited Databases/stocks_by_id_after_editing.csv", index=False)

"""call data editor functions"""
Data_Editor = DataEditor()
Data_Editor.convert_data_columns()
Data_Editor.get_missing_stock_ids()
Data_Editor.remove_stocks_by_id()
