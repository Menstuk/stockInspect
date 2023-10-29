import pandas as pd
import numpy as np
from datetime import datetime


class DataExplorer:

    # find how many NaN values there are:
    def count_nan_values(self, table):
        nan_count = table.isnull().sum().sum()
        return nan_count

    # function that calculates the number of missing rows:
    def missing_dates_detection(self, data):
        gap_sizes_table = []
        gap_sizes_list = []

        date_gaps = 0
        missing_dates = 0
        for row in range(1, len(np.array(data))):
            first_date = datetime.strptime(np.array(data)[row][1], '%d/%m/%Y')
            second_date = datetime.strptime(np.array(data)[row - 1][1], '%d/%m/%Y')
            dif = (first_date - second_date).days
            gap_sizes_list.append(dif - 1)

            if dif > 1:
                date_gaps += 1
                missing_dates = missing_dates + (dif - 1)

        sorted_gap_sizes_list = sorted(gap_sizes_list, reverse=True)
        for gap_size in sorted_gap_sizes_list:
            gap_sizes_table.append([gap_size])

        gap_sizes_table = pd.DataFrame(gap_sizes_table)
        gap_sizes_table.columns = ['Gap Size']

        return gap_sizes_table, date_gaps,
