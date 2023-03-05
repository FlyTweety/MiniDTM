from importlib.metadata import distribution
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

#####################################################################################################################################

def read_data(file_name_list):

    #拆分训练集和测试集
    train_data_path_list = []
    test_data_path_list = []
    for file_name in file_name_list:
        if('iris_test' in file_name):
            test_data_path_list.append(file_name)
        else:
            train_data_path_list.append(file_name)

    train_pd = []
    for i in range(len(train_data_path_list)):
        train_pd.append(pd.read_csv(train_data_path_list[i]))
    test_pd = []
    for i in range(len(test_data_path_list)):
        test_pd.append(pd.read_csv(test_data_path_list[i]))

    # 读取.csv文件
    train_data = pd.concat(train_pd)
    test_data  = pd.concat(test_pd)
    # 去除不需要的第一列序号列
    train_data.drop('Unnamed: 0', axis = 1, inplace = True)
    test_data.drop('Unnamed: 0', axis = 1, inplace = True)

    distribution_number = len(train_data_path_list) #有几份

    return train_data, test_data, distribution_number

#####################################################################################################################################

def train_and_test(train_data, test_data):
    # 0-3列为输入条件，第4列为结果
    x_train = train_data.iloc[:,:4]
    y_train = train_data.iloc[:,4]
    x_test = test_data.iloc[:,:4]
    y_test = test_data.iloc[:,4]
    #训练
    svm = SVC(C=2, gamma = 0.2, kernel='linear', decision_function_shape='ovr')
    svm.fit(x_train, y_train)
    #测试
    score_test = svm.score(x_test, y_test)
    print("测试集的识别率：%s" % score_test)
    score_train = svm.score(x_train, y_train)
    print("训练集的识别率：%s" % score_train)

    return score_test

#####################################################################################################################################

# 蒙特卡洛算法计算ShapleyValue
def Get_ShapleyValue(data_set, test_set, looptimes=100, max_data_size=140):

    #初始化shapley值与累加计数，结尾时累加值除以计数
    SVs = []  
    SV_delta_count = []
    for i in range(0,140):
        SVs.append(0)
        SV_delta_count.append(0)

    #循环looptimes次，每次加一趟SV值
    for looptime in range(0, looptimes):
        print("looptime = ", looptime)
        
        #生成本趟各个点的随机排列
        arrange = gen_random_arrange(max_data_size)
        #训练时y值不能唯一，所以要足够多的数据来保证，生成一个最少的size
        start_size = gen_least_start_size(data_set, arrange)

        #按照随机排列，从前往后生成一趟
        for i in range(start_size, max_data_size): 
            #生成训练集
            set1 = gen_set(data_set, arrange, i)
            set2 = gen_set(data_set, arrange, i-1)
            #训练并测试获取识别准确率
            u1 = gen_accuracy(set1, test_set) 
            u2 = gen_accuracy(set2, test_set)
            #更新Shapley值
            SV_delta = u1 - u2
            SVs[arrange[i]] += SV_delta
            SV_delta_count[arrange[i]] += 1

    #所有趟结束，累加除以计数
    print(SVs)
    print(SV_delta_count)
    for i in range(len(SVs)):
        SVs[i] = SVs[i] / max(SV_delta_count[i], 1)

    #返回Shapley计算结果
    return SVs

# SVM训练测试生成准确率
def gen_accuracy(train_set, test_set):
    # 0-3列为输入条件，第4列为结果
    x_train = train_set.iloc[:,:4]
    y_train = train_set.iloc[:,4]
    x_test = test_set.iloc[:,:4]
    y_test = test_set.iloc[:,4]
    # 训练
    svm = SVC(C=2, gamma = 0.2, kernel='linear', decision_function_shape='ovr')
    svm.fit(x_train, y_train)
    # 测试
    score = svm.score(x_test, y_test) 
    return score    

# 生成0-n随机排列
def gen_random_arrange(data_size):
    arrange = np.arange(data_size)
    np.random.shuffle(arrange)
    return arrange

# 根据随机排列生成所有要用的数据集。前n个就是array[n]
def gen_set(data_set, arrange, data_size):
    dynamic_set = pd.DataFrame(columns=['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Species'])
    for i in range(0, data_size):  #这里是0开始，但是不影响后续
        dynamic_set.loc[i] = data_set.iloc[arrange[i]]
    return dynamic_set

# 生成y值覆盖3个的最小set所需的size
def gen_least_start_size(data_set, arrange):
    i = 0
    start_set = gen_set(data_set, arrange, i)
    while(len(start_set['Species'].unique())<3):
        i += 1
        start_set = gen_set(data_set, arrange, i)
    return i

#####################################################################################################################################

def better_train_and_test(train_data, test_data, SV, bar):
    weights = []
    for sv in SV:
        weights.append(abs(sv))
    choose_set = pd.DataFrame(columns=['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Species'])
    for i in range(len(train_data)):
        if weights[i]>=bar:
            choose_set.loc[len(choose_set)] = train_data.iloc[i]
    print("choose datas amount = ", len(choose_set))
    #训练并测试结果
    score = train_and_test(choose_set, test_data)
    return score

#####################################################################################################################################

def horizontal_federated_learning(file_name_list):
    train_data, test_data, distribution_number = read_data(file_name_list)
    print("distribution_number=", distribution_number)
    SV_3 = Get_ShapleyValue(train_data, test_data, looptimes=2, max_data_size=140)
    SV_3_array = np.array(SV_3)
    mean = np.mean(SV_3_array)
    bar = mean*2
    final_score = better_train_and_test(train_data, test_data, SV_3, bar)
    contribution = [0] * distribution_number
    batch = int( len(SV_3) / distribution_number)
    for i in range(distribution_number):
        for sv in range(batch*i, batch*i+batch):
            if(SV_3[sv] > bar):
                contribution[i] += SV_3[sv]
    contribution_sum = np.sum(contribution)
    real_contribution = [0] * distribution_number
    for i in range(distribution_number):
        real_contribution[i] = contribution[i] / contribution_sum
    return final_score, real_contribution

"""
#测试区
file_name_list = ['C:\\Users\\VitoZCY\\Desktop\\数据要素市场\\final\\datas\\iris_train_1.csv', 'C:\\Users\\VitoZCY\\Desktop\\数据要素市场\\final\\datas\\iris_train_2.csv', 'C:\\Users\\VitoZCY\\Desktop\\数据要素市场\\final\\datas\\iris_test_1.csv', 'C:\\Users\\VitoZCY\\Desktop\\数据要素市场\\final\\datas\\iris_test_2.csv']
final_score, contribution = horizontal_federated_learning(file_name_list)
print(final_score)
print(contribution)
"""