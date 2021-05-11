#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import the needed

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_bokeh
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.models.tools import HoverTool
from bokeh.layouts import column


# Load and wrangle the data

new_data = pd.read_csv("MV_collisions.csv", 
                   parse_dates=True)


# Define Mapping for new weekday column

dw_mapping = {
    0: 'Monday', 
    1: 'Tuesday', 
    2: 'Wednesday', 
    3: 'Thursday', 
    4: 'Friday',
    5: 'Saturday', 
    6: 'Sunday'
} 

# Define Mapping for new month column

look_up = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
            6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}


# Convert date column to datetime

new_data["CRASH DATE"] = pd.to_datetime(new_data["CRASH DATE"])

# Create Total injured column
#num = int(num)  
tot_injured = new_data["NUMBER OF PERSONS INJURED"] + new_data["NUMBER OF PEDESTRIANS INJURED"] + new_data["NUMBER OF MOTORIST INJURED"] 

new_data['tot_injured'] = tot_injured

# Create Total killed column

tot_killed = new_data["NUMBER OF PERSONS KILLED"] + new_data["NUMBER OF PEDESTRIANS KILLED"] + new_data["NUMBER OF MOTORIST KILLED"] 

new_data['tot_killed'] = tot_killed

# Create new columns for day, month, year, hour, day of week

new_data['day'] = new_data['CRASH DATE'].dt.day
new_data['month'] = new_data['CRASH DATE'].dt.month
new_data['month'] = new_data['month'].apply(lambda x: look_up[x])
new_data['year'] = new_data['CRASH DATE'].dt.year
new_data['hour'] = pd.to_datetime(new_data['CRASH TIME'], format='%H:%M').dt.hour
new_data['day_of_week'] = new_data['CRASH DATE'].dt.weekday.map(dw_mapping)


# Drop unwanted columns

new_data = new_data.drop(columns=["LATITUDE", "LONGITUDE", "LOCATION", "ON STREET NAME",
                                  "CROSS STREET NAME", "OFF STREET NAME", "COLLISION_ID",
                                  "VEHICLE TYPE CODE 2", "VEHICLE TYPE CODE 3", "VEHICLE TYPE CODE 4",
                                  "VEHICLE TYPE CODE 5", "ZIP CODE", "CONTRIBUTING FACTOR VEHICLE 1",
                                  "CONTRIBUTING FACTOR VEHICLE 2", "CONTRIBUTING FACTOR VEHICLE 3",
                                  "CONTRIBUTING FACTOR VEHICLE 4", "CONTRIBUTING FACTOR VEHICLE 5",
                                  "NUMBER OF PERSONS KILLED", "NUMBER OF PEDESTRIANS INJURED",
                                  "NUMBER OF PEDESTRIANS KILLED", "NUMBER OF PEDESTRIANS KILLED",
                                  "NUMBER OF CYCLIST INJURED", "NUMBER OF CYCLIST KILLED",
                                  "NUMBER OF MOTORIST INJURED", "NUMBER OF MOTORIST KILLED",
                                  "NUMBER OF PERSONS INJURED"])

# Rename the columns, ready to go

new_data = new_data.rename(columns={"CRASH DATE": "crash_date", "VEHICLE TYPE CODE 1" : "vehicle_type",
                                    "CRASH TIME": "crash_time", "BOROUGH": "borough"})

# Create dataframe with only days with people killed

df2 = new_data[new_data.tot_killed > 2]

# Create interactive chart using Bokeh  figure and line chart

p = figure(plot_height=250, x_axis_type="datetime", tools="", 
           toolbar_location=None,sizing_mode="scale_width", 
           y_range=(2, 15))


p.circle(x='crash_date', y='tot_killed',
         source=df2, size=10, color='#2171b5')


# Set title, axis labels, axis format, background, grid lines

p.title.text = 'Accident with the Highest Fatalities'
p.title.text_font_size = '20pt'
p.background_fill_color="#f5f5f5"
p.grid.grid_line_color="white"

p.xaxis.axis_label = 'Date'
p.xaxis.axis_label_text_font_size = "16pt"
p.xaxis.major_label_text_font_size = "12pt"

p.yaxis.axis_label = 'Crash Deaths'
p.yaxis.axis_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "12pt"


# Set hover tool

hover = HoverTool()
hover.tooltips=[
    ('Borough', '@borough'),
    ('Vehicle Type', '@vehicle_type'),
    ('Weekday', '@day_of_week'),
    ('Month', '@month'),
    ('Day', '@day'),
    ('Year', '@year')
]

p.add_tools(hover)

# This final command is required to launch the plot in the browser

curdoc().add_root(column(p))



# In[ ]:




