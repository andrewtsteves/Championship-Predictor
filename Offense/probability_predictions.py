import models_best_params as M
from sklearn.ensemble import VotingClassifier
import pandas as pd

probs_lr = M.lr.predict_proba(M.X_test)[:, 1]
probs_svc = M.svc.predict_proba(M.X_test)[:, 1]
probs_dt = M.dt.predict_proba(M.X_test)[:, 1]
probs_rf = M.rf.predict_proba(M.X_test)[:, 1]

results = pd.DataFrame({'LR Win Probability': probs_lr * 100,
                       'SVC Win Probability': probs_svc * 100,
                       'DT Win Probability': probs_dt * 100,
                       'RF Win Probability': probs_rf * 100},
                       index = [M.team_year, M.team_index]).round(1)

vote = VotingClassifier(estimators = [('lr', M.lr),
                                      ('svc', M.svc),
                                      ('decisiontree', M.dt),
                                      ('randomforest', M.rf)],
                        voting = 'soft',
                        weights = (0.45 * probs_lr,  0.45 * probs_svc,  0.05 * probs_dt,  0.05 * probs_rf),)

voting = vote.fit(M.X_train, M.y_train)
probs_ens = vote.predict_proba(M.X_test)[:, 1]

prob = pd.DataFrame({'Ensemble Probability': probs_ens}, index = [M.team_year, M.team_index]). round(1)
results = pd.concat([results, prob], axis=1)
#pd.set_option('display.multi_sparse', False)

print(results.to_string())