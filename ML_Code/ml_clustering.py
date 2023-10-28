# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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

# %%
# Data Aggregation
customer_data = main_table.groupby('CustomerID').agg({
    'TransactionID': 'count',
    'Qty': 'sum',
    'TotalAmount': 'sum'
}).reset_index()

# Pilih variabel yang akan digunakan untuk clustering
X = customer_data[['TransactionID', 'Qty', 'TotalAmount']]

# Scaling Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Membuat Model K-Means
kmeans = KMeans(n_clusters=3)
kmeans.fit(X_scaled)

# Menambahkan label cluster ke DataFrame
labels = kmeans.labels_
customer_data['Cluster'] = labels

# Visualisasi Hasil
plt.figure(figsize=(16,8))
plt.scatter(customer_data['Qty'], customer_data['TotalAmount'], c=customer_data['Cluster'], cmap='rainbow')
plt.xlabel('Qty')
plt.ylabel('Total Amount')
plt.title('Clustering menggunakan K-Means')
plt.show()

# %% [markdown]
# Dari visualisasi di atas, Anda dapat melihat bagaimana pelanggan dibagi menjadi beberapa kelompok berdasarkan perilaku pembeliannya.. Misalnya, suatu kelompok mungkin membeli banyak barang, dan total pembayaran yang tinggi mungkin mencerminkan pelanggan yang cenderung menghabiskan uang dalam jumlah besar.. Sebaliknya, klaster dengan jumlah barang yang dibeli sedikit dan jumlah total pembayaran yang rendah mungkin mencerminkan pelanggan membeli dalam jumlah kecil..


