from typing import List
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


class CityWeatherForecastingModel:
    
    def __init__(self,
                 data_df: pd.DataFrame,
                 city_list: List[str],
                 **kwargs):
        self.data = data_df
        self.city_list = city_list
        
        # additional keyword arguments: Train/Test Split
        self.train_start = kwargs.get("train_start", '1960-01-01')
        self.train_end = kwargs.get("train_end", '1999-12-01')
        self.test_start = kwargs.get("test_start", '2000-01-01')
        self.test_end = kwargs.get("test_start", '2013-12-01')
        
        self.train_data = {}
        self.test_data = {}
        self.models = {}
        
    def fit(self):
        for city in self.city_list:
            city_df = self._get_city_data(city)
            # train-test-split
            train, test = self._prepare_train_test_data(city_df)
            # train Holt-Winters model
            self.models[city] = ExponentialSmoothing(train,
                                                     trend="add",
                                                     seasonal="add",
                                                     seasonal_periods=12).fit()
            # store train and test data in attribute
            self.train_data[city] = train
            self.test_data[city] = test
        
    def predict(self,
                city: str,
                target_date: str = None):  # target_date = "2013-12-01" by default
        if len(self.models) == 0:
            raise ValueError("Models not fitted. run 'fit' method first")
        
        if target_date is None:
            target_date = self.test_end
            
        # compute number of data points to predict
        predict_periods = self._get_time_difference_in_months(target_date,
                                                              self.test_start)
        
        predictions = self.models[city].forecast(predict_periods)
        
        return predictions
    
    def plot_predictions(self,
                         city: str,
                         target_date: str = None):
        if target_date is None:
            target_date = self.test_end
        
        # plot train data
        self.train_data[city].plot(legend=True, label="Train Data", figsize=(12,8))
        # plot test data
        self.test_data[city].plot(legend=True, label="True Data")
        # plot predictions
        predictions = self.predict(city, target_date)
        predictions.plot(legend=True, label="Prediction") 

    def _get_city_data(self, city: str):
        return self.data.loc[self.data["City"]==city].copy()
    
    def _prepare_train_test_data(self, data: pd.DataFrame):
        train = data['AverageTemperature'][self.train_start:self.train_end].dropna()
        test = data['AverageTemperature'][self.test_start:self.test_end].dropna()
        return train, test
    
    @staticmethod
    def _get_time_difference_in_months(date_1: str, date_2: str):  # date_1 > date_2
        date_1 = pd.to_datetime(date_1)
        date_2 = pd.to_datetime(date_2)
        
        diff_in_months = (date_1.year - date_2.year) * 12 + (date_1.month - date_2.month)
        return diff_in_months
