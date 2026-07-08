from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import Model_testing as M

param_grid_LR = {'logisticregression__C': [0.0001, 0.001, 0.01, 0.1, 1, 100],
                 'logisticregression__solver': ['lbfgs'],
                 'logisticregression__class_weight': ['balanced'],
                 'logisticregression__max_iter': [1000, 10000, 50000, 100000]}

param_grid_DT = {'decisiontreeclassifier__criterion': ['gini', 'entropy', 'log_loss'],
                 'decisiontreeclassifier__splitter': ['best', 'random'],
                 'decisiontreeclassifier__class_weight': ['balanced'],
                 'decisiontreeclassifier__max_depth': [5, 10, None],}

param_grid_svc = {'svc__C': [0.001, 0.01, 0.1, 1, 100],
                  'svc__kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
                  'svc__class_weight': ['balanced'],
                  'svc__degree': [1, 3, 5, 7]}

param_grid_rf = {'randomforestclassifier__criterion': ['gini', 'entropy', 'log_loss'],
                 'randomforestclassifier__max_depth': [5, 10, None],
                 'randomforestclassifier__class_weight': ['balanced'],
                 }

def search(estimator, param_grid):
    grid = GridSearchCV(estimator = estimator, param_grid = param_grid,
                        scoring = 'balanced_accuracy', cv = 5, n_jobs = -1)
    grid = grid.fit(M.X_train, M.y_train)
    grid_best_params = grid.best_params_
    grid_best_score = grid.best_score_

    random = RandomizedSearchCV(estimator = estimator, param_distributions = param_grid,
                                scoring = 'balanced_accuracy', cv = 5, n_jobs = -1)
    random = random.fit(M.X_train, M.y_train)
    random_best_params = random.best_params_
    random_best_score = random.best_score_

    return grid_best_score, grid_best_params, random_best_score, random_best_params

lr = search(M.pipeline_lr, param_grid_LR)
dt = search(M.pipeline_DT, param_grid_DT)
svc = search(M.pipeline_svc, param_grid_svc)
rf = search(M.pipeline_RF, param_grid_rf)

if __name__ == '__main__':
    print(f'Logistic Regression:')
    print(f'Grid search best score: {lr[0]}')
    print(f'Grid search best params: {lr[1]}')
    print('')
    print(f'Random search best score: {lr[2]}')
    print(f'Random search best params: {lr[3]}')
    print('------------------------------')
    print(f'Decision Tree:')
    print(f'Grid search best score: {dt[0]}')
    print(f'Grid search best params: {dt[1]}')
    print('')
    print(f'Random search best score: {dt[2]}')
    print(f'Random search best params: {dt[3]}')
    print('------------------------------')
    print(f'SVC:')
    print(f'Grid search best score: {svc[0]}')
    print(f'Grid search best params: {svc[1]}')
    print('')
    print(f'Random search best score: {svc[2]}')
    print(f'Random search best params: {svc[3]}')
    print('------------------------------')
    print(f'Random Forest:')
    print(f'Grid search best score: {rf[0]}')
    print(f'Grid search best params: {rf[1]}')
    print('')
    print(f'Random search best score: {rf[2]}')
    print(f'Random search best params: {rf[3]}')