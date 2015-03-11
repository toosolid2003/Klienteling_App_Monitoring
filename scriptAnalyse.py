import numpy as np
import pandas as pd

#Création du dataframe
df = pd.read_excel("/Users/thibaut.segura/Desktop/Raw Data.xlsx")


#Formattage
#####################################################################

#Conversion des entrées de LOGIN_ID en intégrale, quand c'est possible
def formatting(entree):
    try:
        entree = int(entree)
    except:
        pass
    
    return entree

df["LOGIN_ID"] = df.LOGIN_ID.apply(lambda x: formatting(x))

#Filtrage des données de LOGIN_ID: on ne retient que les Sales Associates, parce qu'ils sont au format 'int'
SaRecordings = df[df["LOGIN_ID"].apply(lambda x: type(x) == int)]



#Calculs    
####################################################################
#Nb de transactions réussies
transacOk = SaRecordings["EMPLOYEE_ID"].value_counts().sum()
transacTotal = SaRecordings["LOGIN_ID"].value_counts().sum()
tauxSucces = transacOk / transacTotal

#Type de transactions et nombres (résultat sous forme de Séries, équiv d'un dico)
r = SaRecordings["API_ACTION"].value_counts()

#Nombre de users différents qui sont parvenus à se connecter sur la période
nbUsers = len(SaRecordings["EMPLOYEE_ID"].unique())

#Ratios
###Totaux des recherches
totalSearch = r.sum() - r['Login'] - r['Logout'] - r['Changepwd'] - r['customerDetails']
ItemSearchTotal = r['getInvPar'] + r['getInvStyle'] + r['getInvSku_manual'] + r['getInvSku_picture']

ratioCustomerSearch = r['customerSearch'] / totalSearch
ratioItemSearch = ItemSearchTotal / totalSearch

ratioManualSku = r['getInvSku_manual'] / ItemSearchTotal
ratioSkuPicture = r['getInvSku_picture'] / ItemSearchTotal


#Output
#####################################################################
print('Nombre d\' utilisateurs uniques connectés: ', nbUsers)
print('Taux de succès dans les transactions: ', tauxSucces)
print("Customer Search: ", ratioCustomerSearch, "\n", "Item Search: ", ratioItemSearch)
print('Manual Sku: ', ratioManualSku)
print('SKU with pic: ', ratioSkuPicture)




#Random stuff
#####################################################################

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
