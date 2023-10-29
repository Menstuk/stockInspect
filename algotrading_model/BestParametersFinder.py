import pandas as pd

from BestImputationFinder import BestImputationFinder
from BestNumberOfLookbackFeaturesFinder import BestNumberOfLookbackFeaturesFinder


class BestParametersFinder:
    def __init__(self):
        self.new_full_data = pd.read_csv("C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/read_input_data/new_full_data.csv")
        self.stocks_by_id_after_editing = pd.read_csv("C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/Edited Databases/stocks_by_id_after_editing.csv")
        self.best_imputation_finder = BestImputationFinder()
        self.best_number_of_lookback_features_finder = BestNumberOfLookbackFeaturesFinder()

    def find_best_params(self, rf_starting_params):
        self.best_imputation_finder.find_best_imputation(self.new_full_data, self.stocks_by_id_after_editing, rf_starting_params)
        self.best_number_of_lookback_features_finder.find_best_number_of_lookback_features(self.new_full_data, self.stocks_by_id_after_editing, rf_starting_params)
