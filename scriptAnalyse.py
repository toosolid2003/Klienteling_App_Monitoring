import numpy as np
import pandas as pd
import pygal
import pickle




#1. Formatage des nouvelles données
#####################################################################

#Création du dataframe
df = pd.read_excel("/Users/thibaut.segura/Desktop/Raw Data.xlsx")

#Conversion des entrées de LOGIN_ID en intégrale. Sinon, renvoi d'une valeur nulle
df["LOGIN_ID"] = df["LOGIN_ID"].astype('str').convert_objects(convert_numeric=True)
SaRecordings = df[~df['LOGIN_ID'].isnull()]

#Suppression des colonnes BEFOREWS_TS, END_TS, AFTERWS_TS, TRANSACTION_ID, LOG_INFO et Cus Vs Ite
del SaRecordings["BEFOREWS_TS", "END_TS", "AFTERWS_TS", 'TRANSACTION_ID', "LOG_INFO", "Cus Vs Ite"]

#Conversion du champ START_TS au format datetime, avec création d'une nouvelle colonne "dateTime"
nbLogins = SaRecordings[SaRecordings["API_ACTION"] == "Login"]
SaRecordings["dateTime"] = pd.to_datetime(nbLogins["START_TS"])



#2. Calculs    
####################################################################
#Nb de transactions réussies: si on a un employee ID, alors la transaction est réussie. MMH, à revoir
#A faire: Filtrer les transactions de logins, les compter puis voir lesquelles sont KO avant de faire le ratio

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

#3. Ajout des résultats dans un data frame "Results"
#####################################################################
                   
                   
#4. Prodcutions des graphiques
#####################################################################


#5. Ajout des nouvelles données dans un data frame global 'Raw Data'
#####################################################################
                   
#6. Enregistrement des deux data frames
#####################################################################
                   
                   


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


#Fonctions
def dataViz(resultats, nom):
    '''Creation de graph'''

    #Passage des résultats sous forme de liste
    listeResultats = []
    listeLabels = []

    for cle in resultats.keys():
        listeResultats.append(resultats[cle])
        listeLabels.append(cle)

    #Création d'un objet graphique
    chart = pygal.Line(title=nom, margin=50)
    chart.add('Usage', listeResultats)
    chart.x_labels = listeLabels
    chart.render_to_file('line_chart.svg')
