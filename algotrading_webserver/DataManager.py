from FilesManager import FilesManager
from Predictor import Predictor


class DataManager:

    def __init__(self):
        self.files_manager = FilesManager()
        self.predictor = Predictor()

    def initialize(self):
        self.files_manager.read_input_data()
        self.files_manager.update_stocks_data()
        self.files_manager.prepare_for_prediction(15)
        self.predictor.load_model("C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/algotrading_model/rf_compressed.joblib", self.files_manager.enriched_model_input)
        self.predictor.save_predictions(self.files_manager.new_day_prices, self.files_manager.stocks_by_id)
