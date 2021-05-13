'''
KoBERT 실행 결과 중 val acc가 가장 높은 test acc를 선별하여 7겹 교차 검증의 평균을 구함.
행복+경제('happiness_plus_econ')와 직업+성공('job_plus_success')의 경우를 예시로 보여줌.
'''

import re

def find_top_val_test(folder, data_name):
    top_val = 0
    top_test = 0
    flag = False
    with open('{}/{}.log'.format(folder, data_name), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'val acc' in line:
                #result = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                val = float(re.findall(r"0.\d+", line)[0])
                if val > top_val:
                    top_val = val
                    flag = True
                    top_test = 0
                    #print("val", top_val)
                elif val == top_val:
                    top_val = val
                    flag = True
                elif val < top_val:
                    flag = False
                #print(flag)
            if ('test acc' in line) and flag:
                test = float(re.findall(r"0.\d+", line)[0])
                if test > top_test:
                    top_test = test
                    #print("test", top_test)

    return top_val, top_test


def result_summary(folder, data_name):
    print("======================")
    print(folder)
    print("======================")
    test_list = []
    for i in range(7):
        top_val, top_test = find_top_val_test(folder, "{}_{}".format(data_name, i))

        print("{}_{}".format(data_name, i))
        print("final top val:", round(top_val, 5))
        print("final top test:", round(top_test, 5))
        print("----------------------")

        test_list.append(top_test)
    #print(test_list)
    avg = sum(test_list) / len(test_list) 

    print(folder, "avg:", round(avg, 5), '\n')


pairs = [['result_happiness_plus_econ', 'happiness_plus_econ'], 
         ['result_job_plus_success', 'job_plus_success']]

for folder, data_name in pairs:
    result_summary(folder, data_name)


'''

(term_onto) heeryon@desktop:~/Documents/KIPS_2021_Spring/result_kobert$ python find_top_acc_kobert.py 
======================
result_happiness_plus_econ
======================
happiness_plus_econ_0
final top val: 0.625
final top test: 0.625
----------------------
happiness_plus_econ_1
final top val: 0.5625
final top test: 0.625
----------------------
happiness_plus_econ_2
final top val: 0.625
final top test: 0.625
----------------------
happiness_plus_econ_3
final top val: 0.5625
final top test: 0.875
----------------------
happiness_plus_econ_4
final top val: 0.6875
final top test: 0.5
----------------------
happiness_plus_econ_5
final top val: 0.8125
final top test: 0.375
----------------------
happiness_plus_econ_6
final top val: 0.625
final top test: 0.6875
----------------------
result_happiness_plus_econ avg: 0.61607 

======================
result_job_plus_success
======================
job_plus_success_0
final top val: 0.54167
final top test: 0.375
----------------------
job_plus_success_1
final top val: 0.54167
final top test: 0.4375
----------------------
job_plus_success_2
final top val: 0.47917
final top test: 0.39583
----------------------
job_plus_success_3
final top val: 0.47917
final top test: 0.5
----------------------
job_plus_success_4
final top val: 0.4375
final top test: 0.5625
----------------------
job_plus_success_5
final top val: 0.52083
final top test: 0.4375
----------------------
job_plus_success_6
final top val: 0.47917
final top test: 0.5625
----------------------
result_job_plus_success avg: 0.46726 

(term_onto) heeryon@desktop:~/Documents/KIPS_2021_Spring/result_kobert$ 

'''
