import Stat_record_dependecies as st
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix

offensive_data = st.offensive_data

X = offensive_data.drop(columns = ['Team', 'SB Winner', 'Year'])
y = offensive_data['SB Winner']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 10, stratify = y)

#Logistic Regression
pipeline_lr = make_pipeline(StandardScaler(), LogisticRegression(class_weight = 'balanced'))
pipeline_lr = pipeline_lr.fit(X_train, y_train)
y_pred_lr = pipeline_lr.predict(X_test)
score_lr = pipeline_lr.score(X_test, y_test)
matrix_lr = confusion_matrix(y_test, y_pred_lr)
cvs_lr = cross_val_score(pipeline_lr, X_train, y_train, cv = 10)

#Decision Tree
pipeline_DT = make_pipeline(StandardScaler(), DecisionTreeClassifier(class_weight = 'balanced'))
pipeline_DT = pipeline_DT.fit(X_train, y_train)
y_pred_DT = pipeline_DT.predict(X_test)
score_DT = pipeline_DT.score(X_test, y_test)
matrix_DT = confusion_matrix(y_test, y_pred_DT)
cvs_DT = cross_val_score(pipeline_DT, X_train, y_train, cv = 10)

#Random Forrest Model
pipeline_RF = make_pipeline(StandardScaler(), RandomForestClassifier(class_weight = 'balanced'))
pipeline_RF = pipeline_RF.fit(X_train, y_train)
y_pred_RF = pipeline_RF.predict(X_test)
score_RF = pipeline_RF.score(X_test, y_test)
matrix_RF = confusion_matrix(y_test, y_pred_RF)
cvs_RF = cross_val_score(pipeline_RF, X_train, y_train, cv = 10)

#Support vector classifier model
pipeline_svc = make_pipeline(StandardScaler(), SVC(class_weight = 'balanced'))
pipeline_svc = pipeline_svc.fit(X_train, y_train)
y_pred_svc = pipeline_svc.predict(X_test)
score_svc = pipeline_svc.score(X_test, y_test)
matrix_svc = confusion_matrix(y_test, y_pred_svc)
cvs_svc = cross_val_score(pipeline_svc, X_train, y_train, cv = 10)

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

if __name__ == "__main__":
    print(f"Logistic Regression score: {score_lr}")
    print(f"Cross validation score: {cvs_lr}")
    print(f"Logistic Regression confusion matrix: {matrix_lr}")

    print(f"Decision Tree score: {score_DT}")
    print(f"Cross validation score: {cvs_DT}")
    print(f"Decision Tree confusion matrix: {matrix_DT}")

    print(f"Random Forest score: {score_RF}")
    print(f"Cross validation score: {cvs_RF}")
    print(f"Random Forest confusion matrix: {matrix_RF}")

    print(f"SVC score: {score_svc}")
    print(f"Cross validation score: {cvs_svc}")
    print(f"SVC confusion matrix: {matrix_svc}")

    print(f"MLP score: {score_MLP}")
    print(f"Cross validation score: {cvs_MLP}")
    print(f"MLP confusion matrix: {matrix_MLP}")