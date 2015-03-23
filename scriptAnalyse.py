
# coding: utf-8

## Preparation of data
import pandas as pd
import numpy as np
import pygal


# Création du dataframe
df = pd.read_excel("/Users/thibaut.segura/Desktop/Raw Data.xlsx")
df["EMPLOYEE_ID"] = df["EMPLOYEE_ID"].astype('str').convert_objects(convert_numeric=True)
SaRecordings = df[~df['EMPLOYEE_ID'].isnull()]


# Nombre d'utilisateurs uniques

nbUniqueUsers = len(SaRecordings["EMPLOYEE_ID"].unique())


## Nb de requêtes 'Item Search' total
itemSearch = SaRecordings.query('API_ACTION == ["getInvStyle","getInvSku_manual","getInvSku_manual","getInvSku_picture"]')
iSearch = itemSearch["DAY"].value_counts()
iSearch = iSearch.sort_index()

## Nb de requêtes 'Customer Search' total
df2 = SaRecordings[SaRecordings["API_ACTION"] == "customerSearch"]
cSearch = df2["DAY"].value_counts()
cSearch = cSearch.sort_index()

## Nombre de requêtes par user
userCusto = cSearch.apply(lambda x: x/nbUniqueUsers)
userItem = iSearch.apply(lambda x: x/nbUniqueUsers)

print("Customer Searches per user:\n", userCusto) 
print("Item Searches per user:\n", userItem)

## Sortie graphique



## Classement des utilisateurs les plus actifs



