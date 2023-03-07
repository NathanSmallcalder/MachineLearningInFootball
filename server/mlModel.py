from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from matplotlib import *
import sys
from pylab import *
import seaborn as sns
import mysql.connector
from config import *
import pandas
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

connection = mysql.connector.connect(host=host,
                                     database= sql_user,
                                     user=sql_user,
                                     password=sql_password)

query = ("SELECT `SummonerMatchTbl`.ChampionFk, `MatchStatsTbl`.`MinionsKilled`,`MatchStatsTbl`.`kills`,`MatchStatsTbl`.`deaths`,`MatchStatsTbl`.`assists`,`MatchStatsTbl`.Lane,`MatchStatsTbl`.`DmgDealt`,`MatchStatsTbl`.`DmgTaken`,`MatchStatsTbl`.`TurretDmgDealt`,`MatchStatsTbl`.`TotalGold`,`MatchStatsTbl`.EnemyChampionFk,  `MatchTbl`.`GameDuration`,`MatchStatsTbl`.`DragonKills`,`MatchStatsTbl`.`BaronKills` ,`MatchStatsTbl`.`Win` FROM `SummonerMatchTbl` JOIN `MatchStatsTbl`ON `MatchStatsTbl`.SummonerMatchFk = `SummonerMatchTbl`.SummonerMatchId JOIN `MatchTbl` ON `MatchTbl`.`MatchId` = `SummonerMatchTbl`.`MatchFk` WHERE `MatchTbl`.`QueueType` = 'CLASSIC';")
cursor = connection.cursor()

cursor.execute(query)
data = cursor.fetchall()

columns = ['ChampionFk', 'MinionsKilled','kills','deaths','assists','lane','DmgDealt','DmgTaken','TurretDmgDealt','TotalGold'
,'EnemyChampionFk', 'GameDuration','DragonKills','BaronKills','Win']

#data = pd.read_csv("data.csv")
df_games = pandas.DataFrame(data,columns = columns)
df_games.sample(frac=1)

df_games['lane'] = df_games['lane'].map({'TOP':0,'JUNGLE':1,'MIDDLE':2,'BOTTOM':3,'NONE':4})
df_games['Win'] = df_games['Win']
print(df_games)

X = df_games.drop('Win', axis=1)
y = df_games['Win']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)




importances = rf.feature_importances_
std = np.std([rf.feature_importances_ for tree in rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))



row = [[1,24 ,1,60,1,2,5255,255,1,2000,52,2000,0,0]]

yhat = rf.predict(row)
print('Prediction: %d' % yhat[0])


# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
print(rf.feature_names_in_)
plt.barh(rf.feature_names_in_, rf.feature_importances_)
plt.savefig("Fig.png")