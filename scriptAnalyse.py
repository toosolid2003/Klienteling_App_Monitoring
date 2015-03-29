
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


def visitorsDay(SaRecordings):
    '''Input: Filtered dataframe - SaRecordings - with only recordings from sales associates.
    Output: a Series with unique users, who managed to log in at least once during the day'''
    
    #Filter: only select recordings with a successful login by an SA.
    usersJour = SaRecordings[(SaRecordings["API_ACTION"]=="Login") & (SaRecordings["RESULT_STATUS"]=="OK")]
    
    #On isole les doublons, au cas où quelqu'un se soit connecté deux fois dans la même journée.
    #usersJour = usersJour["LOGIN_ID"].drop_duplicates()
    
    #Grouping results by day
    usersJour = usersJour[["ORGANIZATION_ID","LOGIN_ID","DAY"]].groupby("DAY")
    
    #Computing and returning the number of recordings per day.
    return usersJour.size()


def searchBrand(df, req):
    '''Computes the number of API ACTIONS performed by Sales Associates, brand by brand. 
    Input: 
        - df = a dataframe with only the recordings from Sales Associates
        - req = a list of API ACTION to count per day and per brand
    
    Output: a dataframe with the number of searches, split by brands.'''
    
    #Prepare request
    start = "API_ACTION==['"
    middle = "','".join(req)
    end = "']"
    
    request = start+middle+end
    
    #Select only the API ACTIONS for the search parameters
    items = df.query(request)
    iGroup = items.groupby("DAY")
    
    
    #Group & count the values per brands. Unstack them to have a plottable dataframe.
    searchBrands = iGroup["ORG NAME"].value_counts().unstack()
    searchBrands = searchBrands.fillna(0)
    
    #Add a "Total" column to the dataframe
    indx = searchBrands.columns
    
    searchBrands["Total"] = 0
    for elt in indx:
        searchBrands["Total"] += searchBrands[elt]
    
    return searchBrands

def totalCalls(SaRecordings):
    '''Overall number of calls to the API, per brand. 
    
    Input:  dataframe with only recordings from SAs.
    Output: group object.'''
    
    group = sa[["API_ACTION","ORG NAME"]].groupby("ORG NAME")
    totalCalls = group.size()
    
    return totalCalls


def usageCsv(iSearch, cSearch):
    '''Takes two Series as input and outputs a csv file with number of customer and item searches per day'''
    
    plotData1 = pd.DataFrame(data=iSearch, columns=["ItemSearch"])
    plotData2 = pd.DataFrame(data=cSearch, columns=["CustomerSearch"])
    plotData = pd.merge(plotData1, plotData2, left_index=True, right_index=True)
    plotData.to_csv("usage.csv", headers=True)

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

    
    ######################################################################################################
## Other KPIs
## Most active users
def mostActiveUser(SaRecording):
    '''Input: dataframe (SaRecordings)
    Output: classement des utilisateurs ayant généré le plus de requêtes.'''
    
    use = SaRecording[["LOGIN_ID","API_ACTION"]]

    usergroup = use.groupby('LOGIN_ID')

    return usergroup.size()


## Most active brands
def mostActiveBrands(SaRecording):
    '''Input: dataframe (SaRecordings)
    Output: classement des marques ayant généré le plus de requêtes.'''
    
    brandUse = SaRecording[["ORGANIZATION_ID","API_ACTION", "ORG NAME"]]

    brandUseGroup = brandUse.groupby("ORG NAME")

    return brandUseGroup.size()

#old functions
######################################################################################################

def CustomerSearch(df):
    '''Takes a dataframe as input and returns a Series of Customer Searches, sorted by dates.'''
    
    df2 = df[df["API_ACTION"] == "customerSearch"]
    cSearch = df2["DAY"].value_counts()
    cSearch = cSearch.sort_index()
    
    return cSearch


def ItemSearch(df):
    '''Takes a dataframe as input and returns a Series of Item Searches, sorted by dates.'''
    
    itemSearch = df.query('API_ACTION == ["getInvStyle","getInvSku_manual","getInvSku_picture"]')
    iSearch = itemSearch["DAY"].value_counts()
    iSearch = iSearch.sort_index()
    
    return iSearch

