########################################################################################################################################

import numpy as np
from libsvm.svmutil import *
import os
# 从文件中加载数据，转化为特定格式
def load_data(file_name_list):

    #找出test文件并在列表中删去
    for file_name in file_name_list:
        if('_test' in file_name):
            test_data_path = file_name
            file_name_list.remove(file_name)
    print(file_name_list)
    #现在剩下都是train的文件，拼成一个，保存路径为train_data_path
    train_data_path = os.getcwd()+'//datas//vertical_train_collect.txt'
    for file in file_name_list:
        with open(file, 'r') as f1:
            lines = f1.read().splitlines()
        with open(train_data_path, 'a+') as f2:
            for line in lines:
                print(line, file = f2)
    
    Y_train, X_train = svm_read_problem(train_data_path) #第一列是类别，后面是训练样本
    for idx, y in enumerate(Y_train): #enumerate(Y_train)：(0, Y_train[0])((1, Y_train[1]))
        if y < 0:   #也就是按循序把-1转成0，+1转成1
            Y_train[idx] = 0
        else:
            Y_train[idx] = 1
    #到这Y_train就是一维的list全是01，X_train是一行一个字典组成的列表
    X_train_array = np.array(to_array(X_train))
    #X_train_array每行是一个len=123的list, 原先字典里对应1的位置标为1, 其他都是0
    #下面是对测试数据的处理，同理
    Y_test, X_test = svm_read_problem(test_data_path)
    for idx, y in enumerate(Y_test):
        if y < 0:
            Y_test[idx] = 0
        else:
            Y_test[idx] = 1
    X_test_array = np.array(to_array(X_test))
    return X_train_array, Y_train, X_test_array, Y_test


#字典转成一维列表
def to_array(X_libsvm, file_name='adult'):
    feature_num = 0
    if file_name == 'adult':
        feature_num = 123 
    res = [] 
    for X in X_libsvm:
        X_real = []
        X = dict(X)
        # 123 features
        for i in range(1, feature_num + 1):
            if X.get(i) != 1:
                X_real.append(0)
            else:
                X_real.append(1)
        res.append(X_real)
    return res
    
#原来的array是没有,的（np.array），这个会转成有',', 一共client_num份，每份同样是二维的n行
def split_data(X_train, X_test, client_num):
    feature_num = len(X_test[0])
    each_client_f_num = feature_num // client_num #向下取整的除
    X_train_s = [X_train[:, each_client_f_num * i: each_client_f_num * (i + 1)]
                 for i in range(client_num)]
    X_test_s = [X_test[:, each_client_f_num * i: each_client_f_num * (i + 1)]
                for i in range(client_num)]
    return X_train_s, X_test_s

def softmax(x):
#"""Compute the softmax of vector x
    exp_x = np.exp(x)
    softmax_x = exp_x / np.sum(exp_x)
    return softmax_x 

########################################################################################################################################

class Client(object):
    def __init__(self, X_train, X_test, config) -> None:
        self.X_train = X_train
        self.X_test = X_test

        # Extract config info
        self.batch_size = config['batch_size']
        self.lr = config['learning_rate']
        self.class_num = config['class_num']

        # Init client's params
        self.batch_indexes = [0] * self.batch_size
        feature_num = len(X_test[0])
        self.weight = np.random.random(size=(self.class_num, feature_num))
        self.embedding_grads = np.random.random(size=(self.class_num, self.batch_size))
        self.id = None

    def set_id(self, client_id):
        self.id = client_id

    def set_batch_indexes(self, batch_indexes):
        self.batch_indexes = batch_indexes

    def set_embedding_grads(self, embedding_grads):
        self.embedding_grads = embedding_grads

    # Update weight param of the model
    def update_weight(self):
        self.weight = self.weight + np.dot(self.embedding_grads, self.X_train[self.batch_indexes])
        new_weight = np.zeros(shape=(self.class_num, len(self.X_test[0])))
        for i in range(len(self.weight)):  #应有class_num行
            weight_line_sum = np.sum(self.weight[i])
            for j in range(len(self.weight[i])):
                new_weight[i][j] = self.weight[i][j] / weight_line_sum
        self.weight = new_weight

    def get_embedding_data(self, period_type="batch"):
        """
        Return the embedding data, calculated on X.
        """
        if period_type == 'batch':
            X_batch = self.X_train[self.batch_indexes]
            res = np.dot(self.weight, X_batch.T)  # (class_num, batch_size)
        else:
            # 'test'
            res = np.dot(self.weight, self.X_test.T)  # (class_num, test_size)  
            #weight是class_num*feature_num  X_test是test_size*feature_num  weight*X_test.T是class_num*test_size
            #
        return res

########################################################################################################################################

from typing import List
class Server(object):
    def __init__(self, Y_train, Y_test, config) -> None:
        # Save label data
        self.Y_train = Y_train
        self.Y_test = Y_test

        # Extract config info
        self.class_num = config['class_num']
        self.client_num = config['client_num']
        self.epoch_num = config['epoch_num']
        self.batch_size = config['batch_size']
        self.lr = config['learning_rate']

        self.data_num = len(Y_train)

        # Empty list used to collect clients
        self.clients = list()

        self.bias = np.random.random(size=self.class_num)  #bias是个随机数列，长度=class_num(class_num是结果有多少类)

        self.embedding_data = np.zeros(shape=(self.client_num,
                                              self.class_num, self.batch_size))
        # For test eval
        self.test_embedding_data = np.zeros(shape=(self.client_num,
                                                   self.class_num, len(self.Y_test))) #client_num组，每组是class_num行，每行len(self.Y_test)个

        self.batch_indexes = [0] * self.batch_size

        # w.r.t each client's embedding data
        self.embedding_grads = np.zeros(shape=(self.class_num, self.batch_size))

        self.loss = 0

    def attach_clients(self, clients: List[Client]):
        """ Attach clients to the server. 
        The server can access the client by id.
        """
        self.clients = clients

    def update_embedding_data(self, client: Client, period_type='batch'):
        """ Call client to calculate embedding data and send it to server.
        Server will receive it and save it.
        """
        if period_type == 'test':
            self.test_embedding_data[client.id] = client.get_embedding_data(period_type)
        if period_type == 'batch':
            self.embedding_data[client.id] = client.get_embedding_data(period_type)

    def send_embedding_grads(self, client: Client, grads):
        self.clients[client.id].set_embedding_grads(grads)  #这里对于所有的client，发送的都是同一个grad，这个应该是对所有featrue的

    ##TODO 必要的完成训练的服务端函数
    def cal_batch_embedding_grads(self):

        grads = np.zeros(shape=(self.class_num, self.batch_size))
        aggr_embedding_data = np.sum(self.test_embedding_data, axis=0)
        
        for i in range(0, self.batch_size):
        # Ground truth
            y = self.Y_train[self.batch_indexes[i]]
            # y = X^T \dot weight + bias
            pred_prob = softmax(aggr_embedding_data[:, i] + self.bias)
            self.loss -= np.log(pred_prob[y])  # more right prob, less loss

            # Wrong direction, the higher the more deviant
            grads[:, i] = pred_prob * self.lr
            # Right direction
            grads[y, i] -= 1 * self.lr

        self.embedding_grads = grads

########################################################################################################################################

def vfl_lr_train(server: Server, clients: List[Client]):

    #TODO 完成训练流程
    #就是写一个循环，每次都计算一个新的梯度(自己写的函数)，然后send_embedding_grads发送给client，然后client去update weight，然后服务器update_embedding_data(包含client的get_embedding_data计算)
    
    final_acc = -1

    for i in range(0,10):

        test_loss, test_acc = evaluation(server, clients)
        print('[*info] Current Test Loss %f Current Test Acc: %f' % (test_loss, test_acc))

        server.cal_batch_embedding_grads()
        for client in server.clients:
            server.send_embedding_grads(client, server.embedding_grads)
            client.update_weight()
            server.update_embedding_data(client, period_type='batch')

        if i == 9:
            final_acc = test_acc    

    print("final_acc=", final_acc)
    return final_acc


def evaluation(server: Server, clients: List[Client]):
    # Show the performance on Test Dataset
    test_loss = 0
    test_acc = 0
    for c in clients:
        server.update_embedding_data(c, period_type="test")  #从client获取embedding_data，其中client的embedding_data是weight点乘X_test.T 
        #相当于把server.embedding_data[client.id]取得了一个计算得到的矩阵

    aggr_embedding_data = np.sum(server.test_embedding_data, axis=0) #把上面从不同客户端获得的值累加  
    #所以aggr_embedding_data是几维？？  #axis为0是压缩行,即将每一列的元素相加,将矩阵压缩为一行

    for idx, y in enumerate(server.Y_test):
        # softmax:归一化 [:idx]从0开始idx个 bias是个随机数列，长度=class_num(class_num是结果有多少类)
        pred_prob = softmax(aggr_embedding_data[:, idx] + server.bias)  #在给的测试里,len(bias)=2，可是aggr_embedding_data不是一个class_num * test_size吗
        
        test_loss -= np.log(pred_prob[y])
        if np.argmax(pred_prob) == y:
            test_acc += 1

    test_acc /= len(server.Y_test)

    return test_loss, test_acc

########################################################################################################################################

def fun_vertical_federated_learning(file_name_list):

    # load data
    X_train, Y_train, X_test, Y_test = load_data(file_name_list)

    # config
    config = dict()
    config['class_num'] = 2  #结果有几类
    config['client_num'] = 2  #客户端有几个
    config['epoch_num'] = 5  
    config['batch_size'] = 2000  
    config["learning_rate"] = 0.2561

    # Split Data
    X_train_s, X_test_s = split_data(X_train, X_test, config['client_num'])

    # Init server
    server = Server(Y_train, Y_test, config)

    # Init clients
    clients = list()
    for i in range(config['client_num']):
        c = Client(X_train_s[i], X_test_s[i], config)
        c.set_id(i)
        clients.append(c)

    server.attach_clients(clients)

    # Train and Evaluation
    final_acc = vfl_lr_train(server, clients)
    evaluation(server, clients)

    return final_acc

#测试区
#print("result:")
#print(vertical_learning(['C:\\Users\\VitoZCY\\Desktop\\数据要素市场\\final\\datas\\vertical_train_1.txt', 'C:\\Users\\VitoZCY\\Desktop\\数据要素市场\\final\\datas\\vertical_train_2.txt', 'C:\\Users\\VitoZCY\\Desktop\\数据要素市场\\final\\datas\\vertical_test.txt']))