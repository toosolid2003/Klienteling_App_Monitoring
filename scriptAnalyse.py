
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
    '''Selects only the records created by Sales Associates profiles. Returns a dataframe object.'''
    
    df["LOGIN_ID"] = df["LOGIN_ID"].astype('str').convert_objects(convert_numeric=True)
    SaRecordings = df[~df['LOGIN_ID'].isnull()]
    
    return SaRecordings


def uniqueVisitors():
    nbUniqueUsers = len(SaRecordings["LOGIN_ID"].unique())


def ItemSearch(df):
    '''Takes a dataframe as input and returns a Series of Item Searches, sorted by dates.'''
    
    itemSearch = df.query('API_ACTION == ["getInvStyle","getInvSku_manual","getInvSku_manual","getInvSku_picture"]')
    iSearch = itemSearch["DAY"].value_counts()
    iSearch = iSearch.sort_index()
    
    return iSearch

def itemSearchBrand(df):
    '''Input: a dataframe with only the recordings from Sales Associates
    Output: a dataframe with the split of item searches by brand.'''
    
    #Select only the API ACTIONS for item search
    items = df.query('API_ACTION == ["getInvStyle","getInvSku_manual","getInvSku_manual","getInvSku_picture"]')
    iGroup = items.groupby("DAY")
    
    #Group & count the values per brands. Unstack them to have a plottable dataframe.
    searchBrands = iGroup["ORG NAME"].value_counts().unstack()
    
    return isearchBrands

def CustomerSearch(df):
    '''Takes a dataframe as input and returns a Series of Customer Searches, sorted by dates.'''
    
    df2 = df[df["API_ACTION"] == "customerSearch"]
    cSearch = df2["DAY"].value_counts()
    cSearch = cSearch.sort_index()
    
    return cSearch

def usageCsv(iSearch, cSearch):
    '''Takes two Series as input and outputs a csv file with number of customer and item searches per day'''
    
    plotData1 = pd.DataFrame(data=iSearch, columns=["ItemSearch"])
    plotData2 = pd.DataFrame(data=cSearch, columns=["CustomerSearch"])
    plotData = pd.merge(plotData1, plotData2, left_index=True, right_index=True)
    plotData.to_csv("usage.csv", headers=True)

## Nb of average users per day

## Nb of requests per user:
def averages(search):
    '''Takes the general dataframe and one Series as input and returns a dataframe with the average
    number of requests per user, per day'''
    
    df["LOGIN_ID"]
    
    userCusto = cSearch.apply(lambda x: x/nbUniqueUsers)

    userItem = iSearch.apply(lambda x: x/nbUniqueUsers)

    result = pd.DataFrame()

    result = result.append(iSearch, ignore_index=True)

    result = result.append(cSearch, ignore_index=True)
    
    return result

def visitorsDay(SaRecodings):
    '''Input: Filtered dataframe - SaRecordings - with only recordings from sales associates.
    Output: a Series with unique users, who managed to log in at least once during the day'''
    
    #Filtrage: on sélectionne les entrées qui témoignent qu'un SA s'est connecté avec succès.
    usersJour = SaRecordings[(SaRecordings["API_ACTION"]=="Login") & (SaRecordings["RESULT_STATUS"]=="OK")]
    
    #On isole les doublons, au cas où quelqu'un se soit connecté deux fois dans la même journée.
    #usersJour = usersJour["LOGIN_ID"].drop_duplicates()
    
    #On groupe les entrées par jour.
    usersJour = usersJour[["ORGANIZATION_ID","LOGIN_ID","DAY"]].groupby("DAY")
    
    #Calucl du nombre d'entrée - de "successful logins" - par jour.
    return usersJour.size()


    
    ######################################################################################################
## Other KPIs
## Most active users
def mostActiveUser(SaRecording):
    '''Input: dataframe (SaRecordings)
    Output: classement des utilisateurs ayant généré le plus de requêtes.'''
    
    use = SaRecordings[["LOGIN_ID","API_ACTION"]]

    usergroup = use.groupby('LOGIN_ID')

    return usergroup.size()


## Most active brands
def mostActiveBrands(SaRecording):
    '''Input: dataframe (SaRecordings)
    Output: classement des marques ayant généré le plus de requêtes.'''
    
    brandUse = SaRecordings[["ORGANIZATION_ID","API_ACTION", "ORG NAME"]]

    brandUseGroup = brandUse.groupby("ORG NAME")

    return brandUseGroup.size()

