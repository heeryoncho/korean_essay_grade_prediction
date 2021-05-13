'''
----------------------------------------
실험 구성
----------------------------------------
➀'직업'(훈련)/'직업'(테스트)
➁'직업+경제'(훈련)/'직업'(테스트)
➂'직업+성공'(훈련)/'직업'(테스트)
④'직업+행복'(훈련)/'직업'(테스트)
⑤'직업+경제/성공/행복'(훈련)/'직업'(테스트)
⑥'행복'(훈련)/'행복'(테스트)
⑦'행복+경제'(훈련)/'행복'(테스트)
⑧'행복+성공'(훈련)/'행복'(테스트)
⑨'행복+직업'(훈련)/'행복'(테스트)
⑩'행복+경제/성공/직업'(훈련)/'행복'(테스트)
⑪'통합'(훈련)/'통합'(테스트)

*** '직업'(job), '행복'(happiness), '통합'(all) 테스트 데이터로 성능 평가를 진행함.
*** 각 실험을 진행할 때 val 데이터와 test 데이터는 그대로 둔 채, train 데이터를 다양한 방식으로 혼합함(예를 들어 기존의 train 데이터 끝에 경제 데이터를 결합하여 '직업+경제' 훈련 데이터를 생성.)
'''

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from konlpy.tag import Komoran
from sklearn.metrics import accuracy_score

def get_file(file_name):
    with open(file_name) as f:
        data = pd.read_csv(f, delimiter="\t", quotechar='"')
    return data

def vectorize(train, val, test):
    parser = Komoran()

    temp_train = []
    for doc in train:
        temp_train.append(parser.morphs(doc))
    result_train = [' '.join(tokens) for tokens in temp_train]

    temp_val = []
    for doc in val:
        temp_val.append(parser.morphs(doc.replace("[[문단]] ","")))
    result_val = [' '.join(tokens) for tokens in temp_val]

    temp_test = []
    for doc in test:
        temp_test.append(parser.morphs(doc))
    result_test = [' '.join(tokens) for tokens in temp_test]

    vect = CountVectorizer()
    X_train = vect.fit_transform(result_train)
    X_val = vect.transform(result_val)
    X_test = vect.transform(result_test)

    return X_train, X_val, X_test

# 나이브 베이즈 또는 로지스틱 회귀를 선택하여 실행

clf = MultinomialNB()
#clf = LogisticRegression(random_state=0, max_iter=1000)

#folders = ["all", "happiness", "happiness_plus_econ", "happiness_plus_job", "happiness_plus_success", "happiness_plus_three", "job", "job_plus_econ", "job_plus_happiness", "job_plus_success", "job_plus_three"]

folders = ["happiness_plus_econ", "job_plus_success"]

for folder in folders:
    print("======================")
    print("result_{}".format(folder))
    print("======================")
    
    avg_acc_train = []
    avg_acc_val = []
    avg_acc_test = []    
    
    # 7-fold cross-validation
    for i in range(7):
        train_data_file = "data/{}/train_{}.txt".format(folder, i)
        val_data_file = "data/{}/val_{}.txt".format(folder, i)
        test_data_file = "data/{}/test_{}.txt".format(folder, i)

        data_train = get_file(train_data_file)
        train_doc = data_train["document"].str.replace("[[문단]] ","", regex=True)
        train_label = data_train["label"]

        data_val = get_file(val_data_file)
        val_doc = data_val["document"].str.replace("[[문단]] ","", regex=True)
        val_label = data_val["label"]

        data_test = get_file(test_data_file)
        test_doc = data_test["document"].str.replace("[[문단]] ","", regex=True)
        test_label = data_test["label"]

        X_train, X_val, X_test = vectorize(train_doc, val_doc, test_doc)


        clf.fit(X_train, train_label)
        pred_train = clf.predict(X_train)
        pred_val = clf.predict(X_val)
        pred_test = clf.predict(X_test)

        '''
        print("X_test", X_test.shape)
        print("y_test", len(test_label))
        print("X_val", X_val.shape)
        print("y_val", len(val_label))
        print("X_train", X_train.shape)
        print("y_train", len(train_label))
        '''

        acc_train = accuracy_score(pred_train, train_label)
        avg_acc_train.append(acc_train)

        acc_val = accuracy_score(pred_val, val_label)
        avg_acc_val.append(acc_val)

        acc_test = accuracy_score(pred_test, test_label)
        avg_acc_test.append(acc_test)

        print("acc_train:", round(acc_train, 5))
        print("acc_val:", round(acc_val, 5))
        print("acc_test:", round(acc_test, 5))
        print("-------------------")

    avg_train = sum(avg_acc_train) / len(avg_acc_train)
    avg_val = sum(avg_acc_val) / len(avg_acc_val)
    avg_test = sum(avg_acc_test) / len(avg_acc_test)

    print("AVG_TRAIN:", round(avg_train, 5))
    print("AVG_VAL:", round(avg_val, 5))
    print("AVG_TEST:", round(avg_test, 5))


'''
로지스틱 회귀에서 높은 가중치를 갖는 단어를 발견하는 코드는 ipynb 파일을 참고할 것.

'''
