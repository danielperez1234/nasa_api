# %% [markdown]
# # Load Libraries

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import seaborn as sns
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from prophet import Prophet
import datetime
import os


# %% [markdown]
# # Load Data

# %%
def data_process():
    headers = ['year', 'day', 'hour', 'B_scalar', 'B_magnitude', 'BX_GSE', 'BY_GSE', 'BZ_GSE', 'BY_GSM', 'BZ_GSM', 'SW_temperature', 'SW_proton_density', 'SW_speed', 'flow_pressure', 'Mach_number']
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute file path
    doc = os.path.join(current_directory, 'data2.txt')
    data_raw = pd.read_csv(doc, delim_whitespace=' ', names=headers)

    # Remove rows with missing values
    max_vals = [9999.90, 999.90, 99.90, 999.90, 999.90, 999.90, 999.90, 999.90, 999.90, 999.90, 9999999.00, 999.90, 9999.00, 99.99, 99.90]
    data_raw = data_raw[(data_raw != max_vals).all(axis=1)]
    limit =80000
    data_raw = data_raw[:limit]
    data_raw = data_raw.reset_index(drop=True)
    return data_raw
# %% [markdown]
# # Data Delimitation

# %%

# %% [markdown]
# # Fix Data 4 Prophet

# %%


def get_month_day(numday):
  d0 = datetime.date(1981,1,1)
  deltaT = datetime.timedelta(numday)
  d  = d0 + deltaT
  return d.month, d.day

# Create a dataframe void
def prophet_df(data):
    my_data = pd.DataFrame()


    years = data['year']
    months, days = [], []

    for my_day in data['day']:
      month, day = get_month_day(my_day)
      months.append(month)
      days.append(day)

    # convert years, months, days to string
    years = years.astype(str)
    months = np.array(months).astype(str)
    days = np.array(days).astype(str)

    my_data["ds"] = pd.to_datetime(years + '-' + months + '-' + days, format='%Y-%m-%d')

    # add a column called y with the b_Scalar
    my_data["y"] = data['BZ_GSM']
    return my_data
# %% [markdown]


# ## Find Peaks

# %%
def find_peaks(data):
    data_to_find = data['flow_pressure']
    peaks = sp.signal.find_peaks(data_to_find, height=20, distance=50)
    # plot them
    return peaks

# %% [markdown]
# ## Convert Peaks to Events

# %%
def peaks_event(my_data, peaks):
    special_dates = my_data.iloc[peaks[0]]
    special_dates = special_dates['ds'].astype(str)
    special_dates = special_dates.reset_index(drop=True)

    # create array of strings with the special dates
    events = []
    for date in special_dates:
      events.append(date)

    astronomic_events = pd.DataFrame({
      'holiday': 'astronomic_events',
      'ds': pd.to_datetime(events),
      'lower_window': 0,
      'upper_window': 1,
    })
    return astronomic_events
# %% [markdown]
# ## Add Events to Model

# %%
# Create a new Prophet model with astronomic events
def create_model(astronomic_events, my_data):
    m = Prophet(holidays=astronomic_events)

    # Fit the model to your data
    m.fit(my_data)

    # Make predictions
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    fig = m.plot_components(forecast)
    print(forecast.columns)

    return forecast


# %% [markdown]
# ## Plotting

# %%


def prediction():
    data = data_process()
    profDf = prophet_df(data)
    peaks = find_peaks(data)
    astroEvs = peaks_event(profDf, peaks)
    model = create_model(astroEvs,profDf)



    print(model.head())
    size_big = len(model['ds'])
    percentage = 0.915
    size_small = int(size_big * percentage)
    x = model['ds'][size_small:]
    y = model['yearly'][size_small:]

        # reset index
    x = x.reset_index(drop=True)
    y = y.reset_index(drop=True)

    # find peaks
    data_to_find = y.values
    peaks = sp.signal.find_peaks(data_to_find, height=.05, distance=10)

    # print dates importants
    warning_dates = x.iloc[peaks[0]]
    warning_dates = warning_dates.astype(str)
    warning_dates = warning_dates.reset_index(drop=True).tolist()


    return {'pronostico':{'fechas':x.tolist(), 'valores':y.tolist()},'warning_dates':{'index':peaks[0].tolist(),'valores':warning_dates}}


