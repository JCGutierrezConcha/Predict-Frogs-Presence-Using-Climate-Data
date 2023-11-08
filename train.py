import pickle

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score


# parameters

n_est = 100  # n_estimators
depth = 5    # max_depth
msl = 1    # min_samples_leaf
n_splits = 5
output_file = 'rfc_model.bin'


# data preparation

df = pd.read_csv('frogs_climate_data.csv')

df['occurrenceStatus']=df['occurrenceStatus'].astype(int)
df['q_mean']=np.log1p(df['q_mean'])
df['ppt_mean']=np.log1p(df['ppt_mean'])
df['vpd_mean']=np.log1p(df['vpd_mean'])
df=df.drop(columns=['swe_mean'])

vars=['aet_mean', 'def_mean', 'pdsi_mean', 'ppt_mean', 'soil_mean','tmax_mean', 'tmin_mean',
      'pet_mean', 'q_mean', 'srad_mean', 'vap_mean', 'vpd_mean', 'ws_mean']

df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

# validation

print(f'doing validation')

kfold = KFold(n_splits=n_splits, shuffle=True, random_state=1)

model = RandomForestClassifier(n_estimators=n_est, max_depth= depth, min_samples_leaf = msl,
                             random_state=42, n_jobs=-1)
scores = []

fold = 0

for train_idx, val_idx in kfold.split(df_full_train):
    df_train = df_full_train.iloc[train_idx]
    df_val = df_full_train.iloc[val_idx]

    y_train = df_train.occurrenceStatus.values
    y_val = df_val.occurrenceStatus.values

    model.fit(df_train[vars], y_train)
    y_pred = model.predict_proba(df_val[vars])[:, 1]
    auc = roc_auc_score(y_val, y_pred)
    scores.append(auc)

    print(f'auc on fold {fold} is {auc}')
    fold = fold + 1


print('validation results:')
print('auc = %.3f +- %.3f' % (np.mean(scores), np.std(scores)))

# training the final model

print('training the final model')

df_full_train=df_full_train.reset_index(drop=True)
y_full_train=df_full_train.occurrenceStatus.values
y_test = df_test.occurrenceStatus.values

model.fit(df_full_train[vars], y_full_train)
y_pred = model.predict_proba(df_test[vars])[:, 1]
auc = round(roc_auc_score(y_test, y_pred),3)

print(f'auc={auc}')


# Save the model

with open(output_file, 'wb') as f_out:
    pickle.dump(model, f_out)

print(f'the model is saved to {output_file}')