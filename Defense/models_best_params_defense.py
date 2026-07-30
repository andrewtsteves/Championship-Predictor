import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import Stat_record_dependecies_defense as st

defensive_data = st.defensive_data
defensive_data_shuffled = defensive_data.sample(n = 1643)

X = defensive_data_shuffled.drop(columns = ['SB Winner'])
y = defensive_data_shuffled['SB Winner']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 10, stratify = y)
team_index, team_year = X_test['Team'], X_test['Year']

X_train = X_train.drop(columns = ['Team', 'Year'])
X_test = X_test.drop(columns = ['Team', 'Year'])
y_train = y_train.drop(columns = ['Team', 'Year'])
y_test = y_test.drop(columns = ['Team', 'Year'])

lr = make_pipeline(StandardScaler(),
                   LogisticRegression(C = 0.01, class_weight = 'balanced', random_state = 0,
                                      solver = 'lbfgs', max_iter = 1000))
lr = lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

svc = make_pipeline(StandardScaler(),
                    SVC(C = 100, class_weight = 'balanced', random_state= 1,
                        kernel = 'sigmoid', degree = 5, probability = True))
svc = svc.fit(X_train, y_train)
y_pred_svc = svc.predict(X_test)

dt = make_pipeline(StandardScaler(),
                   DecisionTreeClassifier(splitter = 'random', class_weight = 'balanced',
                                          random_state = 10, criterion = 'gini', max_depth = 5))
dt = dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)

rf = make_pipeline(StandardScaler(),
                   RandomForestClassifier(n_estimators = 1, class_weight = 'balanced', random_state = 1,
                                          criterion = 'gini', max_depth = 5))
rf = rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)