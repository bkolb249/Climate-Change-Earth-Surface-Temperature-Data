"""This file contains all functions and logic for the first part of this
task, i.e. the exploratory data analysis."""
import pandas as pd
from typing import List, Any, Tuple, Union
import matplotlib.pyplot as plt


def get_max_changes_by_country(df: pd.DataFrame,
                               start_year: str = "1850") -> pd.DataFrame:
    """Computes the most severe changes in temperature differences in all
    countries contained in the dataset. The highest change in average
    temperature is considered most severe.

    Args:
        df (pd.DataFrame): The pandas dataframe of the csv-File 
            "GlobalLandTemperaturesByCountry.csv"
        start_year (str, optional): Index of the starting year. Defaults
            to "1850".

    Returns:
        pd.DataFrame: A pandas dataframe with two columns: 
            - 'countries': Country Name 
            - 'MaxChanges': Most Severe Temperature change for that country
    """
    countries = df["Country"].unique()
    max_values = []

    for country in countries:
        # get time series for the country
        df_temp = df.loc[df["Country"]==country]
        # resample & groupby decade to obtain mean for that decade
        df_avg_temp_dec = df_temp[start_year:].resample("10AS").mean()
        # get differences between data points (=Average Temperature per 
        # decade in a country)
        temp_diffs = df_avg_temp_dec["AverageTemperature"].diff()
        # get max value of that country and append to list
        max_values.append(temp_diffs.max())

    return pd.DataFrame(data={"countries": countries,
                              "MaxChanges": max_values})


def calculate_variablity(tmp_series: pd.Series, measure: str) -> Any:
    """ Calculates the given variability measure to a pandas Series

    Args:
        tmp_series (pd.Series): A temperature Series which is to be examined
        measure (str): A measure of variability. Valid choices:
            - "var": Variance
            - "std": Standard Deviation
            - "range": Range
            - "iqr": the IQR

    Raises:
        ValueError: An unknown measure was passed to the function

    Returns:
        float: the measure as a float
    """
    if measure == "var":
        return tmp_series.var()
    elif measure == "std":
        return tmp_series.std()
    elif measure == "range":
        return tmp_series.max() - tmp_series.min()
    elif measure == "iqr":
        return tmp_series.quantile(0.75) - tmp_series.quantile(0.25)
    else:
        error_msg = (f"Unknown variability measure: {measure}. Please choose between: "
                     "'var', 'std', 'range' and 'iqr'.")
        raise ValueError(error_msg)


def get_n_high_variability_cities(input_df: pd.DataFrame,
                                  n: int,
                                  time_from: str,
                                  time_to: str,
                                  return_df: bool,
                                  measure: str = "var",
                                  ) -> Union[Tuple[List, pd.DataFrame], List]:
    """Computes the n cities with the largest value for a given variability
    measure and a given time period.

    Args:
        input_df (pd.DataFrame): The pandas dataframe of the csv-File 
            "GlobalLandTemperaturesByCity.csv"
        n (int): Amount of cities to be returned
        time_from (str): Start of the time_period. Format: "YYYY-MM-DD"
        time_to (str): End of the time_period. Format: "YYYY-MM-DD"
        return_df (bool): Whether to return only the list or also the pandas
            dataframe containing all data
        measure (str, optional): A measure of variability. 
            Valid choices:
                - "var": Variance
                - "std": Standard Deviation
                - "range": Range
                - "iqr": the IQR
            Defaults to "var".
        
    Returns:
        List[str]: List of the top n city names with the highest variability
            measure in the given time period
        pd.Dataframe: result_df, dataframe containing the variability values 
            of all citires in the given time period
    """  
    # subset data
    df = input_df.copy()
    #df_city_temps.loc[(time_from <= df_city_temps.index) & (time_to >= df_city_temps.index)]
    df = df.loc[(time_from <= df.index) & (time_to >= df.index)]
    df = df[["AverageTemperature", "City", "Country"]]
    #, ["AverageTemperature", "City", "Country"]]
    # To avoid duplicate cities (in different countries)
    df["id_City"] = df["City"] + ", " + df["Country"]
    
    # unique cities (Assumption: unique combination of city + country)
    cities = df["id_City"].unique()
    
    variability_measures = []
    
    for city in cities:
        # subset data: time 
        df_city = df.loc[df["id_City"]==city]
        tmp_series = df_city[time_from:time_to]["AverageTemperature"]
        
        variability_measures.append(calculate_variablity(tmp_series, measure))
        
    result_df = pd.DataFrame(data={
        "cities": cities,
        f"variability ({measure})": variability_measures 
    })
    
    result_list = list(result_df.nlargest(n, f"variability ({measure})")["cities"])
    
    if return_df:
        return result_list, result_df
    else:
        return result_list


def plot_city_temp_over_time(df: pd.DataFrame, city: str) -> None:
    """Creates an inline plot of the Yearly Average Temperature of a given
    city, resamplying to yearly data to increase readibility. Addationaly,
    the 10-years rolling mean is depicted

    Args:
        input_df (pd.DataFrame): The pandas dataframe of the csv-File 
            "GlobalLandTemperaturesByCity.csv"
        city (str): The city to plot
    """
    # filter city
    city_df = df.loc[df["City"]==city]
    # resample to yearly data
    city_df_resampled = city_df.resample("AS").mean()
    # obtain rolling mean (10-yearly)
    city_df_resampled["Rolling Avg."] = city_df_resampled.AverageTemperature.rolling(10).mean()
    
    # create plot
    plt.figure()
    city_df_resampled.plot(figsize=(14, 8), title=f"Development of yearly Avg. Temperature for {city}")
    plt.xlabel('Year')
    plt.ylabel('Average Temperature [°C]')
