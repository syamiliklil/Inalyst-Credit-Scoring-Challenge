# -*- coding: utf-8 -*-
"""Inalyst.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ggE1L5rmD0dnN18MDWVJ6iN9VvgrUqeg
"""

from google.colab import files
files.upload()

import os
for dirname, _, filenames in os.walk('/content'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import pandas as pd
import numpy as np

train = pd.read_csv("/content/train.csv")
test = pd.read_csv("/content/test.csv")

train.head()

test.head()

y_train = train['default']
X_train = train.drop('default', axis=1)
X_test = test

X_train['customer_bod'].isnull().values.any()

X_train['gender'].isnull().values.any()
#isi dengan modus

X_train['student'].isnull().values.any()

X_train['employment'].isna().values.any()
#isi dengan modus

X_train['credit_card'].isnull().values.any()
#isi dengan modus

X_train['balance'].isnull().values.any()

X_train['income'].isnull().values.any()

X_train['tenure'].isnull().values.any()

X_train['employment'].fillna(X_train['employment'].mode()[0], inplace=True)
X_train['gender'].fillna(X_train['gender'].mode()[0], inplace=True)
X_train['credit_card'].fillna(X_train['credit_card'].mode()[0], inplace=True)

X_test['employment'].fillna(X_test['employment'].mode()[0], inplace=True)
X_test['gender'].fillna(X_test['gender'].mode()[0], inplace=True)
X_test['credit_card'].fillna(X_test['credit_card'].mode()[0], inplace=True)

X_train.isnull().values.any()

X_test.isnull().values.any()

X_train = X_train.drop(columns=['customer_id'])

X_test = X_test.drop(columns=['customer_id'])

X_train.dtypes

X_train['customer_bod'] =  pd.to_datetime(X_train['customer_bod'])
X_train

X_test['customer_bod'] =  pd.to_datetime(X_test['customer_bod'])
X_test

new_train = X_train["tenure"].str.split(" ", n = 1, expand = True)
new_train.columns = new_train.columns.astype(str)
new_train.rename(columns={'0': 'years', '1':'mons'}, inplace=True)
new_train['years'] = new_train['years'].str.replace('yrs','')
new_train['mons'] = new_train['mons'].str.replace('mon','')
new_train

new_test = X_test["tenure"].str.split(" ", n = 1, expand = True)
new_test.columns = new_test.columns.astype(str)
new_test.rename(columns={'0': 'years', '1':'mons'}, inplace=True)
new_test['years'] = new_test['years'].str.replace('yrs','')
new_test['mons'] = new_test['mons'].str.replace('mon','')
new_test

new_train = new_train.astype(str).astype(int)
new_train.dtypes

new_test = new_test.astype(str).astype(int)
new_test.dtypes

#tenure month/12
new_train['mons'] = new_train['mons'].div(12).round(2)
new_test['mons'] = new_test['mons'].div(12).round(2)
#combine tenure
ten_train = new_train['years'] + new_train['mons']
ten_test = new_test['years'] + new_test['mons']
ten_train

#add to main df
fix_train = pd.concat([X_train, ten_train], axis=1, join='inner')
fix_train.columns = fix_train.columns.astype(str)
fix_train.rename(columns={'0': 'tenure (int)'}, inplace=True)
fix_train = fix_train.drop(columns=['tenure'])
fix_train

#add to main df
fix_test = pd.concat([X_test, ten_test], axis=1, join='inner')
fix_test.columns = fix_test.columns.astype(str)
fix_test.rename(columns={'0': 'tenure (int)'}, inplace=True)
fix_test = fix_test.drop(columns=['tenure'])
fix_test

#bod to age
#Get today's date
import datetime

# Creating dataframe
dfage_train = pd.DataFrame(data = fix_train['customer_bod'])
  
# This function converts given date to age
def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
  
dfage_train = dfage_train['customer_bod'].apply(lambda x: from_dob_to_age(x))

dfage_train.head()

#add to main df
fix_train = pd.concat([fix_train, dfage_train], axis=1, join='inner')

#drop first column
fix_train = fix_train.iloc[: , 1:]

#rename
fix_train.rename(columns={'customer_bod': 'age'}, inplace=True)

fix_train

#bod to age
#Get today's date
import datetime

# Creating dataframe
dfage_test = pd.DataFrame(data = fix_test['customer_bod'])
  
# This function converts given date to age
def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
  
dfage_test = dfage_test['customer_bod'].apply(lambda x: from_dob_to_age(x))

dfage_test.head()

#add to main df
fix_test = pd.concat([fix_test, dfage_test], axis=1, join='inner')

#drop first column
fix_test = fix_test.iloc[: , 1:]

#rename
fix_test.rename(columns={'customer_bod': 'age'}, inplace=True)

fix_test

"""#INGAT
* phone flag ke dummy
* credit card ke dummy
"""

#credit card to object

#phone flag to object

fixfix_train = pd.get_dummies(fix_train)
fixfix_test = pd.get_dummies(fix_test)

fixfix_train

fixfix_train = fixfix_train.astype(float)
fixfix_test = fixfix_test.astype(float)
fixfix_train.dtypes

import matplotlib.pyplot as plt
import seaborn as sns

fig, axs = plt.subplots(ncols=3)
fig.set_size_inches(11.7, 8.27)
sns.boxplot(y=fixfix_train['balance'], ax=axs[0])
sns.boxplot(y=fixfix_train['income'], ax=axs[1])
sns.boxplot(y=fixfix_train['tenure (int)'], ax=axs[2])

y_train

# visualize the target variable
g = sns.countplot(y_train)
g.set_xticklabels(['Not default','Default'])
plt.show()

"""#Modelling
* ROS
* RF
* Gridsearch
"""

from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler()
X_ros, y_ros = ros.fit_sample(fixfix_train, y_train)

X_ros.dtype

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()


classifier = clf.fit(X_ros, y_ros)
predictions = classifier.predict(fixfix_test)[1:,]

predictions

from sklearn.model_selection import GridSearchCV

rfc=RandomForestClassifier()
param_grid = { 
    'n_estimators': [500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,5,6,7,8],
    'criterion' :['gini', 'entropy']
}

CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv= 5)
CV_rfc.fit(X_ros, y_ros)

CV_rfc.best_params_

rfc1=RandomForestClassifier(max_features='log2', n_estimators= 500, max_depth=8, criterion='gini')

classifier1 = rfc1.fit(X_ros, y_ros)
predictions1 = classifier1.predict(fixfix_test)[0:,]
predictions1

import numpy
numpy.savetxt("submission.csv", predictions1, delimiter=",", header='default')

submission_example = pd.read_csv('/content/submission.csv')
submission_example

#indexing
X_index = test
index = test['customer_id']
index

#combine
import pandas as pd

fixsub = pd.concat([index, submission_example], axis=1, join='inner')
fixsub['# default'] = fixsub['# default'].astype(int)
fixsub

fixsub.dtypes
#kayanya dtype nya harus int atau gmn ya

numpy.savetxt("submission.csv", fixsub, delimiter=",", header = 'customer_id,default', comments="")

submission_example = pd.read_csv('/content/submission.csv')
submission_example

submission_example['default'] = submission_example['default'].astype(int)
submission_example['customer_id'] = submission_example['customer_id'].astype(int)

submission_example.to_csv('submission.csv', index = False)
submission_example.dtypes

"""#Model Trial (harusnya didepan_"""

# split imbalanced dataset into train and test sets with stratification
from collections import Counter
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
X_train2, X_test2, y_train2, y_test2 = train_test_split(X_ros, y_ros, test_size=0.2, random_state=1)
print(X_train2.shape, X_test2.shape, y_train2.shape, y_test2.shape)

CV_rfc2 = GridSearchCV(estimator=rfc, param_grid=param_grid, cv= 5)
CV_rfc2.fit(X_train2, y_train2)

CV_rfc2.best_params_

rfc3=RandomForestClassifier(max_features='sqrt', n_estimators= 500, max_depth=8, criterion='gini')

# make predictions
from sklearn.metrics import accuracy_score

yhat = rfc3.fit(X_train2, y_train2)
yhat = CV_rfc2.predict(X_test2)
# evaluate predictions
acc = accuracy_score(y_test2, yhat)
print('Accuracy: %.3f' % acc)