import models_best_params as M
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
pd.set_option('display.multi_sparse', False)