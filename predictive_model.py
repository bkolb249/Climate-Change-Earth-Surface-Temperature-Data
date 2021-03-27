from typing import List, Tuple
from numpy import ndarray
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


class CityWeatherForecastingModel:
    """A wrapper class, which contains n forecasting models for
    n different cities contained in the 
    GlobalLandTemperaturesByCountry.csv file.
    
    Attributes:
        - data (pd.DataFrame): GlobalLandTemperaturesByCountry.csv as as
            pandas dataframe
        - city_list (list): List of all cities for which models are to be 
            created
        - train_start (str): Start date of the training data.
            Format: "YYYY-MM-DD"
        - train_end (str): End date of the training data.
            Format: "YYYY-MM-DD"
        - test_start (str): Start date of the test data.
            Format: "YYYY-MM-DD"
        - test_start (str): End date of the test data.
            Format: "YYYY-MM-DD"
        - train_data (dict): Data the model was trained on.
            Keys are city names
        - test_data (dict): Data the model can be evaluated on
            (not implemented). Keys are city names.
        - models (dict): The trained models for each city. Keys are city names.
            available, after 'fit' method was called.
    """
    
    def __init__(self,
                 data_df: pd.DataFrame,
                 city_list: List[str],
                 **kwargs):
        """Constructor of a CityWeatherForecastingModel.

        Args:
            data_df (pd.DataFrame): GlobalLandTemperaturesByCountry.csv as a
                pandas dataframe
            city_list (List[str]): List of all cities for which models are to
                be created
        
        Additional keyword args (kwargs):
            - train_start (default: '1960-01-01')
            - train_end (default: '1999-12-01')
            - test_start (default: '2000-01-01')
            - test_end (default: '2013-12-01')
        if they are not given, the default values are used.
        """
        self.data = data_df
        self.city_list = city_list
        
        # additional keyword arguments: Train/Test Split
        self.train_start = kwargs.get("train_start", '1960-01-01')
        self.train_end = kwargs.get("train_end", '1999-12-01')
        self.test_start = kwargs.get("test_start", '2000-01-01')
        self.test_end = kwargs.get("test_end", '2013-12-01')
        
        self.train_data = {}
        self.test_data = {}
        self.models = {}
        
    def fit(self):
        """Fits a model for each city in city_list attribute
        """
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
                target_date: str = None) -> ndarray:
        """provides forecast for a given city until target date

        Args:
            city (str): The city for which the weather should be forecasted
            target_date (str, optional): The end of the forecast time horizon.
                If not given, "2013-12-01" is used by default.

        Raises:
            ValueError: If predict method is used before fit method has
                been called

        Returns:
            ndarray: the predictions to each time step
        """
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
                         target_date: str = None) -> None:
        """Create an inline plot of a prediction for the temperature for a 
        given city until the target date.

        Args:
            city (str): The city for which the weather should be forecasted
            target_date (str, optional): The end of the forecast time horizon.
                If not given, "2013-12-01" is used by default.
        """
        if target_date is None:
            target_date = self.test_end
        
        # plot train data
        self.train_data[city].plot(legend=True, label="Train Data", figsize=(12,8))
        # plot test data
        self.test_data[city].plot(legend=True, label="True Data")
        # plot predictions
        predictions = self.predict(city, target_date)
        predictions.plot(legend=True, label="Prediction") 

    def _get_city_data(self, city: str) -> pd.DataFrame:
        """Filters the complete dataframe for one city
        """
        return self.data.loc[self.data["City"]==city].copy()
    
    def _prepare_train_test_data(self,
                                 data: pd.DataFrame
                                 ) -> Tuple[pd.Series, pd.Series]:
        """prepares train and test data:
            - split data
            - drop missing values
            - select only 'AverageTemperature' column
        """
        train = data['AverageTemperature'][self.train_start:self.train_end].dropna()
        test = data['AverageTemperature'][self.test_start:self.test_end].dropna()
        return train, test
    
    @staticmethod
    def _get_time_difference_in_months(date_1: str, date_2: str) -> int: 
        """Computes the time difference in months between two dates. 
        necessary, because forecast-method of model takes number of datapoints
        to forecast as an input. 

        Args:
            date_1 (str): Date in the format 'YYYY-MM-DD'. date_1 > date_2
            date_2 (str): Date in the format 'YYYY-MM-DD'. date_1 > date_2

        Returns:
            int: Difference between the dates in months
        """
        date_1 = pd.to_datetime(date_1)
        date_2 = pd.to_datetime(date_2)
        
        diff_in_months = (date_1.year - date_2.year) * 12 + (date_1.month - date_2.month)
        return diff_in_months
