from __future__ import division
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

# Note this script runs independent of the app.

'''
' Extract the features from an example
'''
def extract_features_etc(example):
    arr = np.zeros(9)
    id_val = arr[0]
    real_class = example[len(example)-1]
    for i in range(1,10):
        arr[i-1] = example[i]
    return arr, id_val, real_class   

'''
' For testing
'''
def signs(a, b):
    predicted = 1.0
    if(a < 0):
        predicted = -1.0
    if(predicted == b):
        #print('returning: '+str(predicted))
        return 1
    return 0

'''
' Train on a set of pre-classified crimes for best parameter values.
'''
def train_classifier(train, vs, test):
    train_set = train 
    valid_set = vs
    test_set = test
    num_steps = 100
    max_epochs = 50
    block = 0
    step_a_param = 0.02
    step_b_param = 50
    lda = 1
    ### Algorithm ###
    lda_arr = [1, 10**-1, 10**-2]
    #accuracies = np.zeros((1,500))
    acc_num = 0

    final_a = None
    final_b = None
    for row in range(0,2):
        a = np.zeros(9)
        b = 0
        lda = lda_arr[row]
        acc_num = 0
        print(lda)
        for r in range(max_epochs): # epochs
            np.random.shuffle(train_set)
            sub_valid_set = train_set[0:50]
            sub_train_set = train_set[50:]
            for k in range(100): # steps
                w = np.random.randint(433)
                x, id_val, yi = extract_features_etc(sub_train_set[w])   
                gamma = (a).dot(x) + b
                step_len = step_a_param / (r+step_b_param)
                ak = np.zeros(9)
                bk = 0
                val = np.zeros(9)
                if (yi * (a.dot(x)+b)) >= 1:
                    val1 = lda*a
                    val2 = 0
                else:
                    val1 = lda*a - yi*x
                    val2 = -yi
                ak = a - step_len*val1
                bk = b - step_len*val2
                a = ak.copy()
                b = bk
                block += 1
                final_a = a.copy()
                final_b = b
    return final_a, final_b # the winners!

# RUN
# train_classifier('train.txt', 'valid.txt', 'test.txt')



