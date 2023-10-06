import joblib
import pandas as pd


class Predictor:

    def __init__(self):
        self.predictions = []
        self.new_day_preds_df = pd.DataFrame()

    def load_model(self, path, enriched_model_input):
        loaded_rf = joblib.load(path)
        self.predictions = loaded_rf.predict(enriched_model_input.iloc[:, enriched_model_input.columns != 'id'])

    """arrange stock ids and predictions in DataFrame. Save to csv file."""
    def save_predictions(self, new_day_prices, stocks_by_id):
        stock_ids = new_day_prices['id']
        curr_closing_prices = new_day_prices['close_price']
        ticker = [stocks_by_id.loc[stocks_by_id['id'] == id, 'stock'].iloc[0] for id in stock_ids]
        ids_preds_dict = {'id': stock_ids, 'ticker': ticker, 'closing_price': curr_closing_prices, 'prediction': self.predictions}
        self.new_day_preds_df = pd.DataFrame(ids_preds_dict)
        self.new_day_preds_df.to_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/model_output/new_day_predictions.csv', index=False)

