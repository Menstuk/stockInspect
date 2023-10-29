import joblib
import pandas as pd


class Predictor:

    def __init__(self):
        self.predictions = pd.DataFrame(columns=['Id', 'Prediction'])
        self.new_day_preds_df = pd.DataFrame()

    def load_model(self, paths_list, enriched_model_input, num_of_days_before_dict):

        for path in paths_list:
            stock_id = int(path.split(sep='_')[5])
            enriched_stock = enriched_model_input.loc[enriched_model_input['id'] == stock_id].copy()
            loaded_rf = joblib.load(path)
            self.predictions.loc[len(self.predictions)] = pd.Series({'Id': stock_id,
                                                                     'Prediction': loaded_rf.predict(enriched_stock.loc
                                                                                                     [:, 'close_price':f'{num_of_days_before_dict[stock_id]}_days_ago'])[0]
                                                                     })
        self.predictions['Id'] = self.predictions['Id'].astype(int)

    """arrange stock ids and predictions in DataFrame. Save to csv file."""
    def save_predictions(self, new_day_prices, stocks_by_id):
        stock_ids = new_day_prices['id'].tolist()
        curr_closing_prices = new_day_prices['close_price'].tolist()
        predictions = self.predictions['Prediction'].tolist()
        ticker = [stocks_by_id.loc[stocks_by_id['id'] == id, 'stock'].iloc[0] for id in stock_ids]
        ids_preds_dict = {'id': stock_ids, 'ticker': ticker, 'closing_price': curr_closing_prices, 'prediction': predictions}
        self.new_day_preds_df = pd.DataFrame(ids_preds_dict)
        self.new_day_preds_df.to_csv(
            'C:/Users/manor/Desktop/Final Project - Algotrading/First Developement Step/output_data/model_output/new_day_predictions.csv', index=False)

