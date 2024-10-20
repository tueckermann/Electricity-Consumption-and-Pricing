

# File names:
# sahkon-hinta-010121-240924.csv
# Electricity_20-09-2024.csv

# 1. Change time format of both files to Pandas datetime

import pandas as pd
import os

path_a= os.getcwd() + '/Data/sahkon-hinta-010121-240924.csv'
df_a = pd.read_csv(path_a)

path_b= os.getcwd() + '/Data/Electricity_20-09-2024.csv'
df_b = pd.read_csv(path_b, sep=';', decimal=',')

df_a['Time'] = pd.to_datetime(df_a['Time'].str.strip(),format = '%d-%m-%Y %H:%M:%S')
df_b['Time'] = pd.to_datetime(df_b['Time'].str.strip(),format = '%d.%m.%Y %H:%M')

# Format in sahkon-hinta: 01-01-2021 00:00:00
# Format in Electricity: 1.1.2020 0:00

# 2. Join the two data frames according to time
# drop the data that doesn't have price (year 2020)
df_ab=pd.merge(df_a, df_b, on='Time',how='left')

# 3. Calculate the hourly bill paid (using information about the price and the consumption)  

df_ab['Electricity bill (€)'] = (df_ab['Price (cent/kWh)'] * df_ab['Energy (kWh)']) / 100

# - Calculated grouped values of daily, weekly or monthly consumption, bill, average price and average temperature
df_ab.rename(columns={
    'Price (cent/kWh)': 'Hourly Price (cent/kWh)',
    'Energy (kWh)': 'Electricity consumption (kWh)',
    'Temperature': 'Avg Temperature (°C)'
}, inplace=True)

df_ab.set_index('Time', inplace=True)

daily = df_ab.resample('D').agg({
    'Electricity consumption (kWh)': 'sum',
    'Electricity bill (€)': 'sum',
    'Hourly Price (cent/kWh)': 'mean',
    'Avg Temperature (°C)': 'mean'
}).reset_index()


weekly = df_ab.resample('W').agg({
    'Electricity consumption (kWh)': 'sum',
    'Electricity bill (€)': 'sum',
    'Hourly Price (cent/kWh)': 'mean',
    'Avg Temperature (°C)': 'mean'
}).reset_index()


monthly = df_ab.resample('M').agg({
    'Electricity consumption (kWh)': 'sum',
    'Electricity bill (€)': 'sum',
    'Hourly Price (cent/kWh)': 'mean',
    'Avg Temperature (°C)': 'mean'
}).reset_index()


# CREATE A VIZUALIZATION INCLUDING...
import streamlit as st
import matplotlib.pyplot as plt
st.title('Electricity Consumption and Pricing')
# 1. A selector for time interval included in the analysis
start_date = st.date_input("Start time", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End time", pd.to_datetime("2024-06-01"))

# Filter the DataFrame based on the selected date range
filtered_df = df_ab[(df_ab.index >= pd.to_datetime(start_date)) & (df_ab.index <= pd.to_datetime(end_date))]

# 2. Consumption, bill, average price and average temperature over selected period
def resample_data(df, interval):
    return df.resample(interval).agg({
        'Electricity consumption (kWh)': 'sum',
        'Electricity bill (€)': 'sum',
        'Hourly Price (cent/kWh)': 'mean',
        'Avg Temperature (°C)': 'mean'
    }).reset_index()

# 3. Selector for grouping interval 

interval_mapping = {
    'Daily': 'D',
    'Weekly': 'W',
    'Monthly': 'M'
}
interval = st.selectbox("Averaging period:", ['Daily', 'Weekly', 'Monthly'])

# Group the data based on the selected interval and calculate totals and averages
grouped_df = resample_data(filtered_df, interval_mapping[interval])
total_consumption = grouped_df['Electricity consumption (kWh)'].sum()
total_bill = grouped_df['Electricity bill (€)'].sum()
avg_hourly_price = grouped_df['Hourly Price (cent/kWh)'].mean()
avg_paid_price = (total_bill / total_consumption) * 100

# Display total consumption, total bill, average hourly price, and average paid price
st.write(f"Total consumption over the period: {total_consumption:.2f} kWh")
st.write(f"Total bill over the period: {total_bill:.2f} €")
st.write(f"Average hourly price: {avg_hourly_price:.2f} cents")
st.write(f"Average paid price: {avg_paid_price:.2f} cents")

# 4. Line graph of consumption, bill, average price and average temperature 
# over the range selected using the grouping interval selected. 
min_time = grouped_df['Time'].min()
max_time = grouped_df['Time'].max()
# Electricity Consumption (kWh)
plt.figure(figsize=(10, 6))
plt.plot(grouped_df['Time'], grouped_df['Electricity consumption (kWh)'], label='Consumption (kWh)', color='blue')
plt.xlabel('Time')
plt.ylabel('Electricity Consumption (kWh)') 
# plt.title('Electricity Consumption Over Time')
plt.xlim(min_time, max_time)
plt.legend()
plt.grid()
st.pyplot(plt)

# Average Hourly Price (cents)
plt.figure(figsize=(10, 6))
plt.plot(grouped_df['Time'], grouped_df['Hourly Price (cent/kWh)'], label='Avg Hourly Price (cents)', color='blue')
plt.xlabel('Time')
plt.ylabel('Average Electricity Price (cents)')
# plt.title('Average Hourly Price Over Time')
plt.xlim(min_time, max_time)
plt.legend()
plt.grid()
st.pyplot(plt)

# Electricity Bill (€)
plt.figure(figsize=(10, 6))
plt.plot(grouped_df['Time'], grouped_df['Electricity bill (€)'], label='Electricity Bill (€)', color='blue')
plt.xlabel('Time')
plt.ylabel('Electricity Bill (€)')
# plt.title('Electricity Bill Over Time')
plt.xlim(min_time, max_time)
plt.legend()
plt.grid()
st.pyplot(plt)

# Average Temperature (°C)
plt.figure(figsize=(10, 6))
plt.plot(grouped_df['Time'], grouped_df['Avg Temperature (°C)'], label='Temperature (°C)', color='blue')
plt.xlabel('Time')
plt.ylabel('Average Temperature (°C)')
# plt.title('Average Temperature Over Time')
plt.xlim(min_time, max_time)
plt.legend()
plt.grid()
st.pyplot(plt)




# st.write("### Electricity Consumption (kWh)")
# st.line_chart(grouped_df.set_index('Time')['Electricity consumption (kWh)'])

# st.write("### Average Hourly Price (cents)")
# st.line_chart(grouped_df.set_index('Time')['Hourly Price (cent/kWh)'])

# st.write("### Electricity Bill (€)")
# st.line_chart(grouped_df.set_index('Time')['Electricity bill (€)'])

# st.write("### Average Temperature (°C)")
# st.line_chart(grouped_df.set_index('Time')['Avg Temperature (°C)'])