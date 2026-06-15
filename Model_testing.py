import Stat_record_dependecies as st
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix

offensive_data = st.offensive_data

X = offensive_data.drop(columns = ['Team', 'SB Winner', 'Year'])
y = offensive_data['SB Winner']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 10, stratify = y)

#Logistic Regression
model_LR = LogisticRegression(max_iter = 10000)
model_LR = model_LR.fit(X_train, y_train)
y_pred_LR = model_LR.predict(X_test)
score_LR = model_LR.score(X_test, y_test)
matrix_LR = confusion_matrix(y_test, y_pred_LR)
cvs_LR = cross_val_score(model_LR, X_train, y_train, cv = 10)

print(f"Logistic Regression score: {score_LR}")
print(f"Cross validation score: {cvs_LR}")
print(f"Logistic Regression confusion matrix: {matrix_LR}")

#Decision Tree
model_DT = DecisionTreeClassifier(class_weight = 'balanced')
model_DT = model_DT.fit(X_train, y_train)
y_pred_DT = model_DT.predict(X_test)
score_DT = model_DT.score(X_test, y_test)
matrix_DT = confusion_matrix(y_test, y_pred_DT)
cvs_DT = cross_val_score(model_DT, X_train, y_train, cv = 10)

print(f"Decision Tree score: {score_DT}")
print(f"Cross validation score: {cvs_DT}")
print(f"Decision Tree confusion matrix: {matrix_DT}")

#Random Forrest Model
model_RF = RandomForestClassifier(class_weight = 'balanced')
model_RF = model_RF.fit(X_train, y_train)
y_pred_RF = model_RF.predict(X_test)
score_RF = model_RF.score(X_test, y_test)
matrix_RF = confusion_matrix(y_test, y_pred_RF)
cvs_RF = cross_val_score(model_RF, X_train, y_train, cv = 10)

print(f"Random Forest score: {score_RF}")
print(f"Cross validation score: {cvs_RF}")
print(f"Random Forest confusion matrix: {matrix_RF}")

#Multi-layered Perceptron classifier
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_MLP = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=10000)
model_MLP = model_MLP.fit(X_train_scaled, y_train)
y_pred_MLP = model_MLP.predict(X_test_scaled)
score_MLP = model_MLP.score(X_test_scaled, y_test)
matrix_MLP = confusion_matrix(y_test, y_pred_MLP)
cvs_MLP = cross_val_score(model_MLP, X_train_scaled, y_train, cv = 10)

print(f"MLP score: {score_MLP}")
print(f"Cross validation score: {cvs_MLP}")
print(f"MLP confusion matrix: {matrix_MLP}")