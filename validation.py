from sklearn.model_selection import (StratifiedKFold, RepeatedStratifiedKFold,
                                     cross_val_score, cross_validate)
from sklearn.metrics import classification_report
import Model_testing as M

classifier_labels = ['Logistic Regression', 'Support Vector Machine',
          'Decision Tree', 'Random Forest']
scoring_types = ['accuracy', 'average_precision', 'recall', 'f1', 'roc_auc']

classifiers = [M.pipeline_lr, M.pipeline_svc, M.pipeline_DT, M.pipeline_RF]
scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

skf = StratifiedKFold(n_splits = 10, shuffle = True)
rskf = RepeatedStratifiedKFold(n_splits = 10, n_repeats = 10)

if __name__ == '__main__':
    for clf, label, in zip(classifiers, classifier_labels):
        print(f'{label}:')
        for scoring_type in scoring_types:
            scores = cross_val_score(clf, M.X_train, M.y_train, scoring = scoring_type,
                                    cv = rskf, n_jobs = -1, error_score = 0)

            print(f'{scoring_type}: {scores.mean():.3f}' 
                  f'+/- {scores.std():.3f}')
        print(f'_________________________')