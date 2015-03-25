
# coding: utf-8

import pandas as pd

import numpy as np



# Create the dataframe:
def mergeData():
    '''Takes the DB extract, merges it with brand labels and returns a dataframe object'''
    
    df1 = pd.read_excel("/Users/thibaut.segura/Desktop/Raw Data.xlsx")

    df2 = pd.read_excel("/Users/thibaut.segura/Desktop/corr.xlsx", sheetname="Corresp")

    df = pd.merge(df1, df2, how='left')

    return df

def getSAonly(df):
    '''Selects only the records created by Sales Associates profiles. Returns a dataframe object'''
    
    df["EMPLOYEE_ID"] = df["EMPLOYEE_ID"].astype('str').convert_objects(convert_numeric=True)
    SaRecordings = df[~df['EMPLOYEE_ID'].isnull()]
    
    return SaRecordings


#ojdeojeoje
nbUniqueUsers = len(SaRecordings["EMPLOYEE_ID"].unique())


def ItemSearch(df):
    '''Takes a dataframe as input and returns a Series of Item Searches, sorted by dates'''
    
    itemSearch = df.query('API_ACTION == ["getInvStyle","getInvSku_manual","getInvSku_manual","getInvSku_picture"]')
    iSearch = itemSearch["DAY"].value_counts()
    iSearch = iSearch.sort_index()


def CustomerSearch(df):
    '''Takes a dataframe as input and returns a Series of Customer Searches, sorted by dates'''
    
    df2 = df[df["API_ACTION"] == "customerSearch"]
    cSearch = df2["DAY"].value_counts()
    cSearch = cSearch.sort_index()

def usageCsv(iSearch, cSearch):
    '''Takes two Series as input and outputs a csv file with number of customer and item searches per day'''
    
    plotData1 = pd.DataFrame(data=iSearch, columns=["ItemSearch"])
    plotData2 = pd.DataFrame(data=cSearch, columns=["CustomerSearch"])
    plotData = pd.merge(plotData1, plotData2, left_index=True, right_index=True)
    plotData.to_csv("usage.csv", headers=True)



## Nb of requests per user:
def averages(cSearch, iSearch, nbusers):
    '''edeedede'''
    userCusto = cSearch.apply(lambda x: x/nbUniqueUsers)

    userItem = iSearch.apply(lambda x: x/nbUniqueUsers)

    result = pd.DataFrame()

    result = result.append(iSearch, ignore_index=True)

    result = result.append(cSearch, ignore_index=True)
    
    return result


## Most active users
use = SaRecordings[["EMPLOYEE_ID","API_ACTION"]]

usergroup = use.groupby('EMPLOYEE_ID')

usergroup.size()

usergroup.size().describe()

usergroup.size().to_clipboard()


## Most active brands
brandUse = SaRecordings[["ORGANIZATION_ID","API_ACTION", "ORG NAME"]]

brandUseGroup = brandUse.groupby("ORG NAME")

brandUseGroup.size()

