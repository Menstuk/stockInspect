from FilesManager import FilesManager
from Predictor import Predictor
from DataPreprocessor import DataPreprocessor


class DataManager:

    def __init__(self):
        self.files_manager = FilesManager()
        self.predictor = Predictor()
        self.data_preprocessor = DataPreprocessor()

    def initialize(self):
        self.files_manager.read_input_data()
        self.files_manager.update_stocks_data()
        self.files_manager.prepare_for_prediction(self.data_preprocessor)
        self.predictor.load_model(self.files_manager.get_paths_by_ids(), self.files_manager.enriched_model_input, self.files_manager.stock_id_to_days_before)
        self.predictor.save_predictions(self.files_manager.new_day_prices, self.files_manager.stocks_by_id)
