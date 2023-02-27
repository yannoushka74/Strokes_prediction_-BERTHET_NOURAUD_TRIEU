import pymongo
import csv
import json
import sys, getopt, pprint
from pymongo import MongoClient
from pprint import pprint
import pandas as pd

client = pymongo.MongoClient("mongodb://root:example@172.18.0.3:27017")
mydb = client["Electronic_product"]
mycol = mydb["sales"]
mydb.mycol.drop()


# results=mycol.find(projection={ '_id': 0})

# print(list(results))
data = pd.read_csv('./DatafinitiElectronicsProductsPricingData.csv', sep = ",")
columns = data.columns.tolist() 
print(columns)
cols_to_use = columns[:len(columns)-5]
data = data.iloc[:, :-5]

print(cols_to_use)

data.reset_index(inplace=True)
data_dict = data.to_dict("records")

mycol.insert_many(data_dict)

print("Connection Successful")
client.close()