import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataPreprocessor:

    # function that adds missing rows to raw stock data
    def add_missing_dates(self, data, method):
        missing_dates_table = []
        table = np.array(data)
        new_table = []
        new_table_index = 0
        for row in range(len(table)):
            if method == 1:  #### the previous date ####
                if row == 0:
                    new_table.append(table[0])
                    new_table_index = new_table_index + 1
                else:
                    first_date = datetime.strptime(table[row][1], '%d/%m/%Y')
                    second_date = datetime.strptime(table[row - 1][1], '%d/%m/%Y')
                    dif = (first_date - second_date).days

                    if dif > 1:  # there is a gap of at least one date
                        for i in range(1, dif):
                            new_row = []
                            for col in range(len(table[row])):
                                if col == 0:
                                    new_row.append(new_table[new_table_index - 1][col])
                                elif col == 1:
                                    date = datetime.strptime(new_table[new_table_index - 1][col],
                                                             '%d/%m/%Y') + timedelta(
                                        days=1)
                                    new_row.append(date.strftime('%d/%m/%Y'))
                                else:
                                    new_row.append(table[row - 1][col])

                            missing_dates_table.append(new_row)
                            new_table.append(new_row)
                            new_table_index = new_table_index + 1

                    new_table.append(table[row])
                    new_table_index = new_table_index + 1

            if method == 2:  #### average of 2 previous dates ####
                if row == 0:
                    new_table.append(table[0])
                    new_table_index = new_table_index + 1
                elif row == 1:
                    first_date = datetime.strptime(table[row][1], '%d/%m/%Y')
                    second_date = datetime.strptime(table[row - 1][1], '%d/%m/%Y')
                    dif = (first_date - second_date).days

                    if dif > 1:  # there is a gap of at least one date
                        for i in range(1, dif):
                            new_row = []
                            for col in range(len(table[row])):
                                if col == 0:
                                    new_row.append(new_table[new_table_index - 1][col])
                                elif col == 1:
                                    date = datetime.strptime(new_table[new_table_index - 1][col],
                                                             '%d/%m/%Y') + timedelta(
                                        days=1)
                                    new_row.append(date.strftime('%d/%m/%Y'))
                                else:
                                    new_row.append(table[row - 1][col])

                            missing_dates_table.append(new_row)
                            new_table.append(new_row)
                            new_table_index = new_table_index + 1

                    new_table.append(table[row])
                    new_table_index = new_table_index + 1

                else:
                    first_date = datetime.strptime(table[row][1], '%d/%m/%Y')
                    second_date = datetime.strptime(table[row - 1][1], '%d/%m/%Y')
                    dif = (first_date - second_date).days

                    if dif > 1:  # there is a gap of at least one date
                        for i in range(1, dif):
                            new_row = []
                            for col in range(len(table[row])):
                                if col == 0:
                                    new_row.append(new_table[new_table_index - 1][col])
                                elif col == 1:
                                    date = datetime.strptime(new_table[new_table_index - 1][col],
                                                             '%d/%m/%Y') + timedelta(
                                        days=1)
                                    new_row.append(date.strftime('%d/%m/%Y'))
                                else:
                                    new_row.append(np.nanmean(
                                        [new_table[new_table_index - 1][col], new_table[new_table_index - 2][col]]))

                            missing_dates_table.append(new_row)
                            new_table.append(new_row)
                            new_table_index = new_table_index + 1

                    new_table.append(table[row])
                    new_table_index = new_table_index + 1

            if method == 4:  #### average of 4 previous dates ####
                if row == 0:
                    new_table.append(table[0])
                    new_table_index = new_table_index + 1
                elif row in [1, 2, 3]:
                    first_date = datetime.strptime(table[row][1], '%d/%m/%Y')
                    second_date = datetime.strptime(table[row - 1][1], '%d/%m/%Y')
                    dif = (first_date - second_date).days

                    if dif > 1:  # there is a gap of at least one date
                        for i in range(1, dif):
                            new_row = []
                            for col in range(len(table[row])):
                                if col == 0:
                                    new_row.append(new_table[new_table_index - 1][col])
                                elif col == 1:
                                    date = datetime.strptime(new_table[new_table_index - 1][col],
                                                             '%d/%m/%Y') + timedelta(
                                        days=1)
                                    new_row.append(date.strftime('%d/%m/%Y'))
                                else:
                                    new_row.append(table[row - 1][col])

                            missing_dates_table.append(new_row)
                            new_table.append(new_row)
                            new_table_index = new_table_index + 1

                    new_table.append(table[row])
                    new_table_index = new_table_index + 1

                else:
                    first_date = datetime.strptime(table[row][1], '%d/%m/%Y')
                    second_date = datetime.strptime(table[row - 1][1], '%d/%m/%Y')
                    dif = (first_date - second_date).days

                    if dif > 1:  # there is a gap of at least one date
                        for i in range(1, dif):
                            new_row = []
                            for col in range(len(table[row])):
                                if col == 0:
                                    new_row.append(new_table[new_table_index - 1][col])
                                elif col == 1:
                                    date = datetime.strptime(new_table[new_table_index - 1][col],
                                                             '%d/%m/%Y') + timedelta(
                                        days=1)
                                    new_row.append(date.strftime('%d/%m/%Y'))
                                else:
                                    new_row.append(np.nanmean(
                                        [new_table[new_table_index - 1][col], new_table[new_table_index - 2][col],
                                         new_table[new_table_index - 3][col], new_table[new_table_index - 4][col]]))

                            missing_dates_table.append(new_row)
                            new_table.append(new_row)
                            new_table_index = new_table_index + 1

                    new_table.append(table[row])
                    new_table_index = new_table_index + 1

        missing = pd.DataFrame(missing_dates_table, columns=data.columns)

        new_data = new_table
        raw_and_missing = pd.DataFrame(new_data, columns=data.columns)

        return raw_and_missing, missing

    # function that drops stock id column, sets 'date' column as index and converts it to 'datetime' type
    def alter_table(self, df, col_to_index, col_to_drop):
        df.set_index(col_to_index, drop=True, inplace=True)
        df.drop(col_to_drop, inplace=True, axis=1)
        df.index = pd.to_datetime(df.index, format="%d/%m/%Y")

    # CREATE LOOKBACK FEATURES
    # We created a function that new creates features:
    # Each feature represents the stock price on a previous day, starting from the day before to 'n' days before.
    # Finally, the function creates a label column of tomorrow's stock prices.
    def create_features(self, df, n, col_name, new_feature, label):

        # Set prices columns in the past 1 - n days
        for daynumber in range(n):
            df[f'{daynumber + 1}{new_feature}'] = np.nan
            for timestamp, row in df.iterrows():
                curr_date = timestamp.date()
                past_date = curr_date - timedelta(days=daynumber + 1)

                try:
                    df.loc[str(curr_date), f'{daynumber + 1}{new_feature}'] = df.loc[str(past_date), col_name]

                except KeyError:
                    df.loc[str(curr_date), f'{daynumber + 1}{new_feature}'] = np.nan

        # Create a label column - tomorrow's stock prices
        df[label] = df[col_name].shift(-1)

        return df

    # drop all missing dates - since we want to prevent our model from learning the connections between each closing price
    def drop_missing_dates(self, raw_and_missing_new, missing):
        return raw_and_missing_new[~raw_and_missing_new.index.isin(missing.index)]

    # Temporal splitting to train and test:
    def generate_split_date(self, raw_and_missing_new):
        split_row_idx = raw_and_missing_new.shape[0] * 0.8
        split_row = raw_and_missing_new.iloc[int(split_row_idx)]
        split_date = str(split_row.name.date())
        return split_date

    # Since the first n rows and the last n rows have nan values - the model would not be trained on them.
    # Therefore, we created a function that removes these rows. Additionally, it splits the data to X and y:
    def rmv_nans_splt_Xy(self, df, label):

        # remove rows with nans
        df = df.loc[df.notnull().all(axis=1)]

        # split the data to X and y
        X = df[[col for col in df.columns if col != label]]
        y = df[label]

        return X, y