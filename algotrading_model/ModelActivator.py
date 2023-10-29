import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor


class ModelActivator:

    # activate random forest function:
    def run_random_forest(self, X_train, y_train, X_test, y_test, params):

        regr = RandomForestRegressor(**params)

        # train random forest with selected parameters to fit it to data:
        regr.fit(X_train, y_train)

        # get model's predictions:
        y_test_pred = regr.predict(X_test)
        y_train_pred = regr.predict(X_train)

        # calculate mse:
        test_mse = mean_squared_error(pd.array([1]).repeat(len(y_test.values)), y_test_pred / y_test.values)
        # test_mse = mean_squared_error(y_test.values, y_test_pred)

        train_mse = mean_squared_error(y_train.values, y_train_pred)

        return train_mse, test_mse
