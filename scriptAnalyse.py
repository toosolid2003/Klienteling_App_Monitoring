import numpy as np
import pandas as pd

#Création du dataframe
df = pd.read_excel("Raw Data2.xlsx")

#Nombre de visiteurs uniques, Sales Associates uniquement
#####################################################################
#
#loginsAll = df["LOGIN_ID"].unique()
#
#loginsSA = []
#for login in loginsAll:
#    try:
#        loginsSA.append(int(login))
#    except:
#        pass
#    
#print("Nombre de visiteurs uniques totaux: ",len(loginsSA))
#
##Conversion des valeurs "Employee_ID" en intégrale pour distinguer les Sales Assistants des autres users
#s = df["EMPLOYEE_ID"]
#for entree in s:
#    try:
#        s[indX] = int(s[indX])
#    except ValueError:
#        "Mauvaise valeur"
#    indX += 1



#Calculs    
####################################################################
#Nb de transactions réussies
transacOk = df["EMPLOYEE_ID"].value_counts().sum()

#Type de transactions et nombres (résultat sous forme de Séries, équiv d'un dico)
r = df["API_ACTION"].value_counts()

#Ratios
###Totaux des recherches
totalSearch = r['customerSearch'] + r['getInvPar'] + r['getInvStyle'] + r['getInvStyle'] + r['getInvSku_manual'] + r['getInvSku_picture']

ratioCustomerSearch = r['customerSearch'] / totalSearch
ratioItemSearch = (r['getInvPar'] + r['getInvStyle'] + r['getInvStyle'] + r['getInvSku_manual'] + r['getInvSku_picture']) / totalSearch


#Output
#####################################################################
print("Customer Search: ", ratioCustomerSearch, "\n", "Item Search: ", ratioItemSearch)