# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima

# %% [markdown]
# ## Data Preparation and Cleaning

# %%
customer = pd.read_csv('../Datasets/Case Study - Customer.csv',sep=';')
product = pd.read_csv('../Datasets/Case Study - Product.csv',sep=';')
transaction = pd.read_csv('../Datasets/Case Study - Transaction.csv',sep=';')
store = pd.read_csv('../Datasets/Case Study - Store.csv',sep=';')

# transaction.head()
# customer.head()
# product.head()
# store.head()

# %%
# Mengubah tipe data kolom Date pada dataset transaction menjadi datetime
transaction['Date'] = pd.to_datetime(transaction['Date'], format='%d/%m/%Y')

# Mengisi missing value dengan nilai sebelumnya
customer.isna().sum()
customer.fillna(method='ffill', inplace=True)

# membuat tabel utama baru dengan menggabungkan semua tabel
main_table = pd.DataFrame()
main_table = pd.merge(transaction, customer, how='left', on='CustomerID')
main_table = pd.merge(main_table, product, how='left', on='ProductID')
main_table = pd.merge(main_table, store, how='left', on='StoreID')
# main_table.info()
# main_table.isna().sum()
main_table.head()

# %% [markdown]
# ## Grafik

# %%
# Mengelompokkan data berdasarkan tanggal dan menghitung total penjualan harian
daily_sales = main_table.groupby('Date')['Qty'].sum()

plt.figure(figsize=(15, 6))
plt.plot(daily_sales.index, daily_sales.values, marker='.', linestyle='-', color='b')
plt.xlabel('Tanggal')
plt.ylabel('Total Penjualan Harian (Rupiah)')
plt.title('Total Penjualan Harian')
plt.grid(True)
plt.show()

# %%
arima_parameter = auto_arima(daily_sales, seasonal=True, stepwise=True)
print(arima_parameter.order)  # Menampilkan parameter terbaik

p, d, q = arima_parameter.order
model = SARIMAX(daily_sales, order=(p, d, q))
model_fit = model.fit()

# Prediksi
predictions = model_fit.forecast(steps=30)  # Menghasilkan prediksi untuk 30 hari ke depan

# Memperbarui indeks data
predictions.index = pd.date_range(start=daily_sales.index[-1], periods=31, closed='right')

# Visualisasi Hasil
plt.figure(figsize=(12, 6))
plt.plot(daily_sales, label='Data Asli')
plt.plot(predictions, label='Prediksi', color='red')
plt.xlabel('Tanggal')
plt.ylabel('Qty')
plt.legend()
plt.grid(True)
plt.show()


