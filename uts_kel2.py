# -*- coding: utf-8 -*-
"""UTS_kel2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sMF3R_gyjrf3lTMJXV9wdy0I2gzCoDGi
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# supress warnings
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

# Data viz lib
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
from matplotlib.pyplot import xticks

bank = pd.read_csv("/content/drive/MyDrive/DATA MINING/bankmarketing.csv")
bank.head()

bank.columns

# Import kolom kategori
bank_cust = bank[['age','job', 'marital', 'education', 'default', 'housing', 'loan','contact','month','day_of_week','poutcome']]
bank_cust.head()

# Convert age menjadi categorical variable.
bank_cust['age_bin'] = pd.cut(bank_cust['age'], [0, 20, 30, 40, 50, 60, 70, 80, 90, 100], 
                              labels=['0-20', '20-30', '30-40', '40-50','50-60','60-70','70-80', '80-90','90-100'])
bank_cust  = bank_cust.drop('age',axis = 1)
bank_cust.head()

"""**Data Inspection**"""

bank_cust.shape

bank_cust.describe()

bank_cust.info()

"""**Data Cleaning**"""

# Cek nilai null
bank_cust.isnull().sum()*100/bank_cust.shape[0]

# Menyimpan copy data
bank_cust_copy = bank_cust.copy()

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
bank_cust = bank_cust.apply(le.fit_transform)
bank_cust.head()

!pip install KModes

pip install --upgrade kmodes

# Import Library

from kmodes.kmodes import KModes

km_cao = KModes(n_clusters=2, init = "Cao", n_init = 1, verbose=1)
fitClusters_cao = km_cao.fit_predict(bank_cust)

# Predicted Clusters
fitClusters_cao

clusterCentroidsDf = pd.DataFrame(km_cao.cluster_centroids_)
clusterCentroidsDf.columns = bank_cust.columns

clusterCentroidsDf

km_huang = KModes(n_clusters=2, init = "Huang", n_init = 1, verbose=1)
fitClusters_huang = km_huang.fit_predict(bank_cust)

# Predicted clusters
fitClusters_huang

cost = []
for num_clusters in list(range(1,5)):
    kmode = KModes(n_clusters=num_clusters, init = "Cao", n_init = 1, verbose=1)
    kmode.fit_predict(bank_cust)
    cost.append(kmode.cost_)

y = np.array([i for i in range(1,5,1)])
plt.plot(y,cost)

## Choosing K=2
km_cao = KModes(n_clusters=2, init = "Cao", n_init = 1, verbose=1)
fitClusters_cao = km_cao.fit_predict(bank_cust)

fitClusters_cao

"""Menggabungkan predisksi cluster dengan original df"""

bank_cust = bank_cust_copy.reset_index()

clustersDf = pd.DataFrame(fitClusters_cao)
clustersDf.columns = ['cluster_predicted']
combinedDf = pd.concat([bank_cust, clustersDf], axis = 1).reset_index()
combinedDf = combinedDf.drop(['index', 'level_0'], axis = 1)

combinedDf.head()

cluster_0 = combinedDf[combinedDf['cluster_predicted'] == 0]
cluster_1 = combinedDf[combinedDf['cluster_predicted'] == 1]

cluster_0.info()

cluster_1.info()

plt.subplots(figsize = (15,5))
sns.countplot(x=combinedDf['job'],order=combinedDf['job'].value_counts().index,hue=combinedDf['cluster_predicted'])
plt.show()