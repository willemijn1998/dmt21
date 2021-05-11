# Import 
import pandas as pd
import numpy as np 
import csv 
from datetime import datetime
import itertools
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import svm, datasets
from sklearn.linear_model import LogisticRegressionCV
from sklearn import preprocessing
from collections import Counter
from sklearn import tree
from sklearn.model_selection import cross_val_score

# This svm takes all features into account and adds up the temporal data gradually, so e.g. to calculate the average mood for 4 days it 
# sums 0.1 * mood_1 + 0.2*mood_2 + 0.3*mood_3 + 0.4 * mood_4 

dataset = "df_imp.csv" s
df = pd.read_csv(dataset)

# aggregate the dataset 
df_agg = df[df.columns[3:]].multiply((df["t"]+1)*0.1, axis="index")
df_agg[["no", "target"]] = df[["no", "target"]]
df_agg = df_agg.groupby(['no', 'target'], as_index=False).sum()

# create dataframe for features
df_X = df_agg.iloc[:, 2:]

# create numpy arrays with target values
y = df_agg.iloc[:, 1].to_numpy()

c = Counter()
c.update(y)
print(c)

weight = {k: len(y)/v for k, v in c.items()}
print(y)

# Get column names first
names = df_X.columns

# Create the Scaler object
scaler = preprocessing.StandardScaler()
# Fit your data on the scaler object
scaled_df = scaler.fit_transform(df_X)
scaled_df = pd.DataFrame(scaled_df, columns=names)

X = scaled_df.to_numpy()

# train the SVM 
linear = SVC(kernel='linear', C=1, class_weight=weight, random_state=42)
rbf = SVC(kernel='rbf', gamma=1, C=1, random_state=42)
poly = SVC(kernel='poly', degree=3, C=1, random_state=42)
sig = SVC(kernel='sigmoid', C=1, random_state=42)

accuracy_lin = cross_val_score(linear, X, y, cv=10)
accuracy_poly = cross_val_score(poly, X, y, cv=10)
accuracy_rbf = cross_val_score(rbf, X, y, cv=10)
accuracy_sig = cross_val_score(sig, X, y, cv=10)

print("Accuracy Linear Kernel:", (accuracy_lin.mean(), accuracy_lin.std()))
print("Accuracy Polynomial Kernel:", (accuracy_poly.mean(), accuracy_poly.std()))
print("Accuracy Radial Basis Kernel:", (accuracy_rbf.mean(), accuracy_rbf.std()))
print("Accuracy Sigmoid Kernel:", (accuracy_sig.mean(),accuracy_sig.std()))