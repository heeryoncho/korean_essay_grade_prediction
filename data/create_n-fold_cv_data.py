'''

실험 데이터 세트 다운로드 방법:

http://aihumanities.org/ko/archive/data/?vid=1

위 URL에서 "한국어 쓰기 텍스트-점수 구간 데이터 세트 (304건)"이라는 제목의 글에 달린 첨부 파일

	korean_essay_score_range_prediction_dataset.zip (1.74MB)

을 다운로드 하여 data 폴더 안에 배치함.

아래 코드는 위 데이터 세트 중 all.txt, happiness.txt, job.txt로 7겹 교차 검증 데이터 세트를 생성하는 코드임.

'''


from sklearn.model_selection import StratifiedKFold, train_test_split
from pandas import read_csv
import pandas as pd
from pathlib import Path


def create_dataset(data_name):
    Path("{}".format(data_name)).mkdir(parents=True, exist_ok=True)

    data = read_csv('{}.txt'.format(data_name), delimiter='\t')

    X = data.document
    y = data.label

    # 7-fold cross validation
    rs = 6   ### random_state_seed

    skf = StratifiedKFold(n_splits=7, shuffle=True, random_state=rs)
    skf.get_n_splits(X, y)

    n = 0
    for train_index, test_index in skf.split(X, y):
        #print("TRAIN:", train_index, "TEST:", test_index)
        X_rest, X_test = X[train_index], X[test_index]
        y_rest, y_test = y[train_index], y[test_index]
        X_train, X_val, y_train, y_val = train_test_split(X_rest, y_rest, 
                                         test_size=0.17, random_state=rs, stratify=y_rest)
        train = pd.concat([X_train, y_train], axis=1)
        val = pd.concat([X_val, y_val], axis=1)
        test = pd.concat([X_test, y_test], axis=1)
        train.to_csv('{}/train_{}.txt'.format(data_name, n), sep='\t')
        val.to_csv('{}/val_{}.txt'.format(data_name, n), sep='\t')
        test.to_csv('{}/test_{}.txt'.format(data_name, n), sep='\t')
        n = n + 1

data_names = ['all', 'job', 'happiness']

for data_name in data_names:
    create_dataset(data_name)
    
