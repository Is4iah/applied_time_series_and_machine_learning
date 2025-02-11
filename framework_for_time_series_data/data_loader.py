import os.path

import numpy as np
import pandas as pd
import yfinance as yf

from time_series import UnivariateTimeSeries

def build_airline_passenger_uts() -> UnivariateTimeSeries:
    # Get air passenger data and build our UTS
    data_df = pd.read_csv("../datasets/AirPassengers.csv")

    return UnivariateTimeSeries(
        time_col="month",
        time_values=data_df["Month"].values,
        values_cols="passengers_count",
        values=data_df["#Passengers"].values
    )

def build_stock_uts(stock_symbol: str, stock_name: str, start_date: str, end_date: str) -> UnivariateTimeSeries:
    stock_df = yf.download(stock_symbol, start=start_date, end=end_date)

    return UnivariateTimeSeries(
        time_col="Date",
        time_values=stock_df.index,
        values_cols="Open",
        values=stock_df["Open"].values
    )

def build_air_temperature_uts() -> UnivariateTimeSeries:
    data_df = pd.read_csv("../datasets/daily-min-temperatures.csv")

    return UnivariateTimeSeries(
        time_col="Date",
        time_values=data_df["Date"],
        values_cols="Temp",
        values=data_df["Temp"].values
    )

def build_any_univariate_time_series(path_to_file: str) -> UnivariateTimeSeries:
    file_extension = os.path.splitext(path_to_file)[1]

    # add support for if csv file
    # if file_extension == ".csv":
    #     data_df = pd.read_csv(path_to_file)

    if file_extension == ".npy":
        with open(path_to_file, 'rb') as f:
            series = np.load(f)
            data_df = pd.DataFrame(series, columns=['Observations'])
            data_df["Timestamp"] = data_df.index
            data_df.set_index('Timestamp', inplace=True)

        return UnivariateTimeSeries(
            time_col=data_df.index.name,
            time_values=data_df.index,
            values_cols="Observations",
            values=data_df["Observations"].values
        )

    else:
        print("File extension not supported yet. Contact me at dbrinkle@usc.edu so I can add support for this file extension.")
