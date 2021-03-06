"""
Target Problem:
---------------
* A classifier for the diagnosis of Autism Spectrum Disorder (ASD)

Proposed Solution (Machine Learning Pipeline):
----------------------------------------------
* Standard Scaling -> PCA -> Decision Tree Classifier

Input to Proposed Solution:
---------------------------
* Directories of training and testing data in csv file format
* These two types of data should be stored in n x m pattern in csv file format.

  Typical Example:
  ----------------
  n x m samples in training csv file (n number of samples, m - 1 number of features, ground truth labels at last column)
  k x s samples in testing csv file (k number of samples, s number of features)

* These data set files are ready by load_data() function.
* For comprehensive information about input format, please check the section
  "Data Sets and Usage Format of Source Codes" in README.md file on github.

Output of Proposed Solution:
----------------------------
* Predictions generated by learning model for testing set
* They are stored in "submission.csv" file.

Code Owner:
-----------
* Copyright © Team 4. All rights reserved.
* Copyright © Istanbul Technical University, Learning From Data Spring 2019. All rights reserved. """

import csv
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

np.random.seed(1)  # Anchoring randomization during training step


def load_data():

    """
    The method reads train and test file to obtain train and test data.
    Then, it splits train data into two parts which are features and labels.
    :return: features and labels of train data and test data are returned.

    """

    train_data = pd.read_csv('train.csv')
    test_data = pd.read_csv('test.csv')

    all_train = train_data.iloc[:, :].values
    y_train = train_data.iloc[:, 595].values  # labels
    x_train = train_data.iloc[:, 0:595].values  # features

    x_test = test_data.iloc[:, 0:595].values

    return x_train, y_train, x_test


def standardization(x_train, x_test):

    """
    The method performs standard scaling on training and testing data.
    When doing this, only train data is included in training phase (fitting operation).

    Parameters
    ----------
    x_train: features of train data
    x_test: features of test data

    """

    sc = StandardScaler()
    x_train_std = sc.fit_transform(x_train)
    x_test_std = sc.transform(x_test)

    return x_train_std, x_test_std


def dim_red(x_train, x_test):

    """
    The method reduces the dimension of training and testing data by using PCA.
    When doing this, only training data is included in training phase (fitting operation).

    Parameters
    ----------
    x_train: features of scaled training data
    x_test: features of scaled testing data

    """

    pca = PCA(n_components=15)
    x_train_red = pca.fit_transform(x_train)
    x_test_red = pca.transform(x_test)

    return x_train_red, x_test_red


def decision_tree(criterion_name, x_train, y_train, x_test):

    """
    The method creates a decision tree learning model, trains it by using train data and generate predictions for
        testing data.
    Then, predicted labels are returned.

    Parameters
    ----------
    criterion_name: it specifies which function is used to measure quality of a split
    x_train: features of scaled and reduced training set
    y_train: labels of scaled and reduced training set
    x_test: features of scaled and reduced testing set

    """

    dtc = DecisionTreeClassifier(criterion=criterion_name, max_depth=4,
                                 max_features=3, random_state=3, max_leaf_nodes=2)
    dtc.fit(x_train, y_train)
    y_pred = dtc.predict(x_test)

    return y_pred


def write_output(y_pred):

    fields = ['ID', 'Predicted']
    filename = "submission.csv"
    rows = list()
    with open(filename, 'w',newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        for i in range(len(y_pred)):
            rows.append([i+1, y_pred[i]])
        csvwriter.writerows(rows)


# ********** MAIN PROGRAM ********** #

x_train, y_train, x_test = load_data()
x_train_std, x_test_std = standardization(x_train, x_test)
x_train_red, x_test_red = dim_red(x_train_std, x_test_std)

y_pred = decision_tree('entropy', x_train_red, y_train, x_test_red)
write_output(y_pred)
