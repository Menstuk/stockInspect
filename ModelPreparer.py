from BestParametersFinder import BestParametersFinder
from ModelTrainer import ModelTrainer


class ModelPreparer:
    def __init__(self):
        self.best_parameters_finder = BestParametersFinder()
        self.model_trainer = ModelTrainer()
        self.rf_starting_params = {'n_estimators': 100, 'oob_score': True, 'random_state': 0}

    def prepare_models(self):
        self.best_parameters_finder.find_best_params(self.rf_starting_params)
        self.model_trainer.train_models(self.rf_starting_params)


model_preparer = ModelPreparer()
model_preparer.prepare_models()
