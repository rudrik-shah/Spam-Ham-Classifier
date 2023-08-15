#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import math
import os


# In[ ]:


dir = os.getcwd()


# In[ ]:


# Importing the data set
df = pd.read_csv("spam_ham_dataset.csv",header = None)
df


# In[ ]:


# Creating the variables for the dataset
x = df[2]
y = df[3]


# In[ ]:


# Cleaning the dataset (Omit special characters, if any)
c = 0         # To maintain index
for i in x:
    s = ''        # Temporary string variable
    for j in i:
        if((j >= 'a' and j <= 'z') or (j >= 'A' and j <= 'Z') or (j == ' ')):
            s += j        # Take only characters except 
    x[c] = s
    c += 1


# In[ ]:


x_train = x
y_train = y


# In[ ]:


s = 0        # Variable to count number of spam mails
ns = 0        # Variable to count number of non spam mails
ds = {}        # Dictionary to store the spam mail words and their count pairs
dns = {}        # Dictionary to store the non spam mail words and their count pairs
for i in range(1,len(x_train)):
    words = x_train[i].split()        # Split the mails into words list
    temp =[]
    for j in range(0,len(words)):        # To avoid duplicates we take the words that are unique during counting
        if(words[j].lower() not in temp):
            temp.append(words[j].lower())
    
    if(y_train[i] == '0'):        # If the mail is non spam, then increment the word count
        for j in range(0,len(temp)):
            if(temp[j].lower() in dns.keys()):
                dns[temp[j].lower()] += 1
            else:
                dns[temp[j].lower()] = 1
        ns += 1
    else:                         # If the mail is spam, then increment the word count
        for j in range(0,len(temp)):
            if(temp[j].lower() in ds.keys()):
                ds[temp[j].lower()] += 1
            else:
                ds[temp[j].lower()] = 1
        s += 1


# In[ ]:


# To calculate the probability of each word
for i in ds:
    ds[i] /= s
for i in dns:
    dns[i] /= ns


# In[ ]:


# Predicting on test mails
for i in os.listdir("test"):
    with open(os.path.join("test",i),'r')as file:
#         Initially, probability of spam and spam is 1 (1 beacuse we multiply it with itself further)
        ps = 1
        pns = 1
        l = file.readlines()      # reading the lines of the mail one after the other
        for i in range(0,len(l)):
            words = l[i].split()       # Split the words in a line in words
            
#             Calculating the probability of the mail being spam
            for j in ds:
                if((ds[j] > 0) and ds[j] < 1):
                    if(j in words):
                        ps *= ds[j]
                    else:
                        ps *= (1-ds[j])
                    if(ps < 10**(-250)):
                        ps *= 1000
#             Calculating the probability of the mail being non spam
            for j in dns:
                if((dns[j] > 0) and dns[j] < 1):
                    if(j in words):
                        pns *= dns[j]
                    else:
                        pns *= (1-dns[j])
                    if(pns < 10**(-250)):
                        pns *= 1000
#         If probability of spam mail is more then, print 1, otherwise 0                
        if(ps > pns):
            print(1)
        else:
            print(0)

