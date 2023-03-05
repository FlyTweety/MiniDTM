#coding = 'utf-8'

from database_funs import * #数据库有关操作函数

import sys
from PyQt5.QtWidgets import QFileDialog, QButtonGroup, QInputDialog, QLabel, QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QMessageBox, QTableWidget, QAction, QTableWidgetItem, QRadioButton
from PyQt5.QtGui import QFont, QPalette, QPixmap, QBrush, QIcon
from PyQt5.QtCore import Qt
from PyQt5.Qt import *
import re
import pyap
from LAC import LAC
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#文件路径大合集
ICON_PATH = './images/bg_son.jpg'
WELCOME_BG_PATH = "./images/bg_son.jpg"

##卖家界面##################################################################################################################################
class Window_Seller_Main(QDialog):
    def __init__(self):
        super().__init__()
        #获取屏幕分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        #设置窗口大小
        self.HEIGHT = int(self.screenRect.height() * 0.6)
        self.WIDTH = int(self.screenRect.width() * 0.6)
        self.TOP = int(self.screenRect.height() * 0.2)
        self.LEFT = int(self.screenRect.width() * 0.2)
        #从上一级窗口继承的变量
        self.seller_id = None
        #成员变量
        self.model_mode_choose = None
        self.current_ontable_dataset = "None"
        #设置该窗口元素
        self.Init_UI()

    def Init_UI(self):
        #窗口设置
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT) 
        self.setWindowTitle('MiniDTM_Seller')
        self.setWindowIcon(QIcon(ICON_PATH))
        #背景图片
        palette = QPalette()
        pix = QPixmap(WELCOME_BG_PATH)
        pix = pix.scaled(self.width(),self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        #综合显示框
        self.label_table_alldatas = QLabel(self)
        self.label_table_alldatas.setText("Current ontable set is: " + str(self.current_ontable_dataset))
        self.label_table_alldatas.setStyleSheet("color: cornsilk")
        self.label_table_alldatas.setAlignment(Qt.AlignCenter)
        font_label_table_alldatas = QFont()
        font_label_table_alldatas.setPointSize(12)
        font_label_table_alldatas.setBold(True)
        self.label_table_alldatas.setFont(font_label_table_alldatas)
        self.table_alldatas = QTableWidget(self)
        #原始数据集处理部分
        #标题
        self.label_rawdatas = QLabel(self)
        self.label_rawdatas.setText("Raw Datas")
        self.label_rawdatas.setStyleSheet("color: cornsilk")
        self.label_rawdatas.setAlignment(Qt.AlignCenter)
        font_label_rawdatas = QFont()
        font_label_rawdatas.setPointSize(12)
        font_label_rawdatas.setBold(True)
        self.label_rawdatas.setFont(font_label_rawdatas)
        #数据脱敏、合规检查、价格评估、上传入库按钮
        self.bt_rawdatas_upload = QPushButton('Data Upload', self)
        self.bt_rawdatas_upload.clicked.connect(self.rawdatas_upload)
        self.bt_data_desensitization = QPushButton('Data Desensitization', self)
        self.bt_data_desensitization.clicked.connect(self.data_desensitization)
        self.bt_data_compliance = QPushButton('Data Compliance', self)
        self.bt_data_compliance.clicked.connect(self.check_exist_sensitization)
        self.bt_price_evaluaion = QPushButton('Price Evaluaion', self)
        self.bt_price_evaluaion.clicked.connect(self.price_evaluaion)
        #模型部分
        #标题
        self.label_model = QLabel(self)
        self.label_model.setText("Data Model")
        self.label_model.setStyleSheet("color: cornsilk")
        self.label_model.setAlignment(Qt.AlignCenter)
        font_label_model = QFont()
        font_label_model.setPointSize(12)
        font_label_model.setBold(True)
        self.label_model.setFont(font_label_model)
        #输入框与按钮
        self.lineedit_jobname = QLineEdit(self)
        self.lineedit_jobname.setPlaceholderText("input job name here")
        self.bt_choose_vertical = QRadioButton('Vertical',self)
        self.bt_choose_horizonal = QRadioButton('horizonal',self)
        self.bt_group = QButtonGroup(self)
        self.bt_group.addButton(self.bt_choose_vertical, 1)
        self.bt_group.addButton(self.bt_choose_horizonal, 2)
        self.bt_group.buttonClicked.connect(self.bt_group_clicked)
        self.bt_model_upload = QPushButton('Model Upload', self)
        self.bt_model_upload.clicked.connect(self.model_upload)
        #查询部分
        #标题
        self.label_query = QLabel(self)
        self.label_query.setText("Data Query")
        self.label_query.setStyleSheet("color: cornsilk")
        self.label_query.setAlignment(Qt.AlignCenter)
        font_label_query = QFont()
        font_label_query.setPointSize(12)
        font_label_query.setBold(True)
        self.label_query.setFont(font_label_query)
        #输入框和按钮
        self.lineedit_queryset_name = QLineEdit(self)
        self.lineedit_queryset_name.setPlaceholderText("input queryset name here")
        self.lineedit_query_price = QLineEdit(self)
        self.lineedit_query_price.setPlaceholderText("input price per line here")
        self.bt_queryset_upload = QPushButton('Queryset Upload', self)
        self.bt_queryset_upload.clicked.connect(self.queryset_upload)
        #显示布局
        vbox = QVBoxLayout()
        #0 顶部综合框
        vbox.addWidget(self.label_table_alldatas)
        vbox.addWidget(self.table_alldatas)
        #1 原始数据部分
        hbox1 = QHBoxLayout()
        vbox.addWidget(self.label_rawdatas)
        hbox1.addWidget(self.bt_data_desensitization)
        hbox1.addWidget(self.bt_data_compliance)
        hbox1.addWidget(self.bt_price_evaluaion)
        hbox1.addWidget(self.bt_rawdatas_upload)
        vbox.addLayout(hbox1)
        #2 模型部分
        vbox.addWidget(self.label_model)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.lineedit_jobname)
        hbox2.addWidget(self.bt_choose_vertical)
        hbox2.addWidget(self.bt_choose_horizonal)
        hbox2.addWidget(self.bt_model_upload)
        hbox2.addStretch(1)
        vbox.addLayout(hbox2)
        #3 数据查询部分
        vbox.addWidget(self.label_query)
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.lineedit_queryset_name)
        hbox3.addWidget(self.lineedit_query_price)
        hbox3.addWidget(self.bt_queryset_upload)
        hbox3.addStretch(1)
        vbox.addLayout(hbox3)
        #完成布局
        self.setLayout(vbox)
        self.show()


    #原始数据集处理部分函数*****************************************************************************************************************

    #原始数据上传入库(会按空格进行分割)，更新rawdatas表
    def rawdatas_upload(self):
        #上传文件生成字典
        self.format_header, self.format_lines, fname = self.upload_file_into_lines(split_str=" ")

        #将每行字段内容长度对齐
        self.format_lines = self.align_lines(self.format_lines)
        #基于数据的格式自动生成表格显示 需要数据每行的格式都相同
        self.table_alldatas.setColumnCount(len(self.format_header))
        self.table_alldatas.setHorizontalHeaderLabels(self.format_header)
        self.flash_table_datas_from_format_lines(self.table_alldatas, self.format_lines)
        #更新表格标题
        self.current_ontable_dataset = str(fname)
        self.label_table_alldatas.setText("Current ontable set is: " + str(self.current_ontable_dataset))
        print(3)
        #获取该数据集文件名
        print("fanme=",fname)
        """
        rawdata_name = re.findall("^.+/([a-zA-Z0-9]+)\.[a-zA-Z0-9]+$", str(fname))  #这行有问题 找不到
        if(len(rawdata_name)<3):
            rawdata_name = 'temp'+str(np.random.random(0,10000))
        else:
            rawdata_name = rawdata_name[0]
        """
        rawdata_name = 'temp'+str(np.random.randint(1, high=1000000))
        print("rawdata_name=", rawdata_name)
        #检查重名
        db_datas = db_get_table_datas("rawdatas")
        for item in db_datas:
            if(item['name'] == fname):
                QMessageBox.warning(self, "warning", "raw datas already exists!")
                return 1
        #可以继续，同步到库
        row_list = ['name', 'seller']
        value_list = [rawdata_name, str(self.seller_id)]
        db_add_one_row('rawdatas', row_list, value_list)
        QMessageBox.warning(self, "warning", "successfully upload!")
        #目前其实只是上传了个名字

    #数据脱敏 1.上传文本,更新表格(该模式上传不会分割) 2.进行文本识别 3.返回脱敏后文本
    def data_desensitization(self):
        #上传文件生成字典
        self.format_header, self.format_lines, fname = self.upload_file_into_lines()
        print("header=",self.format_header,"\nlines=",self.format_lines)
        #进行脱敏操作
        self.desensitization_format_lines = self.format_lines #这个仅仅为了创建一个非空的同等规模
        #这里默认是按行了，每行没有分割的字符串
        for i in range(len(self.format_lines)):
            self.desensitization_format_lines[i] = self.find_and_replace_sensitive_words(self.format_lines[i])
        #脱敏完毕，将脱敏后文件保存
        QMessageBox.information(self, "notion", "Desensitization done. Please save the datas")
        fileName = QFileDialog.getSaveFileName(self, 'Save desensitization datas', './' ,"All Files (*);;Text files (*.txt)")
        if fileName[0]:
            with open(fileName[0], 'w', errors='ignore') as f:
            #with open(fileName[0], 'w',encoding='gb18030',errors='ignore') as f:
                for line in self.desensitization_format_lines:
                    for item in line:
                        f.write(item+' ')
                    f.write('\n')
        print("desensitization_format_lines=", self.desensitization_format_lines)
        #同时更新表格显示和表格标题 
        self.table_alldatas.setColumnCount(len(self.format_header))
        self.table_alldatas.setHorizontalHeaderLabels(self.format_header)
        self.flash_table_datas_from_format_lines(self.table_alldatas, self.desensitization_format_lines, dimension=1)
        self.current_ontable_dataset = str(fileName[0])
        self.label_table_alldatas.setText("Current ontable set is: " + str(self.current_ontable_dataset))

    #查找敏感元素并进行替换
    def find_and_replace_sensitive_words(self, input):
        #由于编码缘故，中文很迷惑，故不考虑
        #设置电话号码、MAC地址、邮箱、ipv4、IMEI的正则模式
        pattern_phone = re.compile("1(?:3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}", re.DOTALL)
        pattern_mac   = re.compile("[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}", re.DOTALL)
        pattern_email = re.compile("[a-zA-Z0-9]{3}[a-zA-Z0-9]*@[A-Za-z]+\.[A-Za-z0-9]+[\.[A-Za-z0-9]+]?", re.DOTALL)
        pattern_ipv4 = re.compile("(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)", re.DOTALL)
        pattern_IMEI = re.compile("(?:\d[ |\-|\_|\+|\—]*){15}", re.DOTALL)
        patterns = [pattern_phone, pattern_mac, pattern_email, pattern_ipv4, pattern_IMEI]
        #分类正则查找替换
        find_sign = 0
        for i in range(len(patterns)):
            res = re.findall(patterns[i], input)
            if(len(res)!=0):
                find_sign = 1
                if i==0:
                    print("pattern0 in:", input)
                    output = re.sub('1(?:3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{4}(\d{4})', '*******\\1', input)
                elif i==1:
                    print("pattern1 in:", input)
                    output = re.sub('([a-zA-Z0-9]{2})[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}', '\\1:*:*:*:*:*', input)
                elif i==2:
                    print("pattern2 in:", input)
                    output = re.sub('([a-zA-Z0-9]{3})[a-zA-Z0-9]*@([A-Za-z]+\.[A-Za-z0-9]+[\.[A-Za-z0-9]+]?)', '\\1***@\\2', input)
                elif i==3:
                    print("pattern3 in:", input)
                    output = re.sub("(?:(25[0-5]|2[0-4]\d|[01]?\d\d?)\.)(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.)(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.)(?:25[0-5]|2[0-4]\d|[01]?\d\d?)", "\\1.*.*.*", input)
                elif i==4:
                    output = re.sub("(?:\d[ |\-|\_|\+|\—]*){10}(\d[ |\-|\_|\+|\—]*\d[ |\-|\_|\+|\—]*\d[ |\-|\_|\+|\—]*\d[ |\-|\_|\+|\—]*\d[ |\-|\_|\+|\—]*)", "*********\\1", input)
        #查找地址
        res = pyap.parse(input, country='US') #尝试美国
        if(len(res)>0):
            output = "this is a sensitive address" + res[0]
            find_sign = 1
        res = pyap.parse(input, country='CA') #尝试加拿大
        if(len(res)>0):
            output = "this is a sensitive address" + res[0]
            find_sign = 1
        res = pyap.parse(input, country='GB') #尝试英国
        if(len(res)>0):
            output = "this is a sensitive address" + res[0]
            find_sign = 1
        cn_address_list = [] #尝试中国
        lac = LAC(mode="lac") #模式为词性标注与词语识别
        lac_result = lac.run(input)
        for index, lac_label in enumerate(lac_result[1]):
            if lac_label == "LOC":
                cn_address_list.append(lac_result[0][index])
        if(len(cn_address_list)>0):
            output = "this is a sensitive address" + res[0]
            find_sign = 1
        reg_str = '(?:[0-9]+[a-zA-Z]* [a-zA-Z0-9]*|[a-zA-Z0-9]* [0-9]+[a-zA-Z]*), (?:[0-9]+[a-zA-Z]* [a-zA-Z0-9]*|[a-zA-Z0-9]* [0-9]+[a-zA-Z]*), (?:[0-9]+[a-zA-Z]* [a-zA-Z0-9]*|[a-zA-Z0-9]* [0-9]+[a-zA-Z]*), (?:[0-9]+[a-zA-Z]* [a-zA-Z0-9]*, |[a-zA-Z0-9]* [0-9]+[a-zA-Z]*, |)[A-Z][a-z]+'
        pattern = re.compile(reg_str) #用自己参照题目规范里德国地址和谷歌到的欧洲地址格式写的正则
        res = re.findall(pattern, input)
        if(len(res)>0):
            output = "this is a sensitive address" + res[0]
            find_sign = 1
        #都没找到，说明没有敏感元素，将输入直接返回
        if(find_sign==0):
            print("no sensitive element in:", input)
            output = input
        return output

    #数据合规检查，是否包含敏感字符
    def check_exist_sensitization(self):
        #上传文件生成列表
        self.format_header, self.format_lines, fname = self.upload_file_into_lines()
        print("header=",self.format_header,"\nlines=",self.format_lines)
        #获取敏感信息
        self.sensitization_lists = []
        for line in self.format_lines:
            self.sensitization_lists.append(self.find_and_get_sensitive_words(line))
        #同时更新表格显示和表格标题 
        self.table_alldatas.setColumnCount(len(self.format_header))
        self.table_alldatas.setHorizontalHeaderLabels(self.format_header)
        self.flash_table_datas_from_format_lines(self.table_alldatas, self.sensitization_lists, dimension=1)
        self.current_ontable_dataset = str(fname)
        self.label_table_alldatas.setText("Current ontable set is: " + str(self.current_ontable_dataset) + '\'s sensitization')
        #检查如果全是nothing的话，那是合规的。否则不合规
        compliance = True
        for line in self.sensitization_lists:
            if line != 'nothing':
                compliance = False
                break
        if(compliance == True):
            QMessageBox.information(self, "notion", "No sensitization in datas!")
        else:
            QMessageBox.information(self, "notion", "All sensitization has shown on table")

    #查找敏感元素输出
    def find_and_get_sensitive_words(self, input):
        #由于编码缘故，中文很迷惑，故不考虑
        sensitive_words = ""
        #设置电话号码、MAC地址、邮箱、ipv4、IMEI的正则模式
        pattern_phone = re.compile("1(?:3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}", re.DOTALL)
        pattern_mac   = re.compile("[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}[ |\-|_|\+]*:[ |\-|_|\+]*[a-zA-Z0-9]{2}", re.DOTALL)
        pattern_email = re.compile("[a-zA-Z0-9]{3}[a-zA-Z0-9]*@[A-Za-z]+\.[A-Za-z0-9]+[\.[A-Za-z0-9]+]?", re.DOTALL)
        pattern_ipv4 = re.compile("(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)", re.DOTALL)
        pattern_IMEI = re.compile("(?:\d[ |\-|\_|\+|\—]*){15}", re.DOTALL)
        patterns = [pattern_phone, pattern_mac, pattern_email, pattern_ipv4, pattern_IMEI]
        #分类正则查找替换
        find_sign = 0
        for i in range(len(patterns)):
            res = re.findall(patterns[i], input)
            if(len(res)!=0):
                find_sign = 1
                for i in range(len(res)):
                    sensitive_words += ' '
                    sensitive_words += res[i]
        #查找地址
        res = pyap.parse(input, country='US') #尝试美国
        if(len(res)>0):
            output = res[0]
            sensitive_words += " "
            sensitive_words += output
            find_sign = 1
        res = pyap.parse(input, country='CA') #尝试加拿大
        if(len(res)>0):
            output = res[0]
            sensitive_words += " "
            sensitive_words += output
            find_sign = 1
        res = pyap.parse(input, country='GB') #尝试英国
        if(len(res)>0):
            output = res[0]
            sensitive_words += " "
            sensitive_words += output
            find_sign = 1
        cn_address_list = [] #尝试中国
        lac = LAC(mode="lac") #模式为词性标注与词语识别
        lac_result = lac.run(input)
        for index, lac_label in enumerate(lac_result[1]):
            if lac_label == "LOC":
                cn_address_list.append(lac_result[0][index])
        if(len(cn_address_list)>0):
            output = res[0]
            sensitive_words += " "
            sensitive_words += output
            find_sign = 1
        reg_str = '(?:[0-9]+[a-zA-Z]* [a-zA-Z0-9]*|[a-zA-Z0-9]* [0-9]+[a-zA-Z]*), (?:[0-9]+[a-zA-Z]* [a-zA-Z0-9]*|[a-zA-Z0-9]* [0-9]+[a-zA-Z]*), (?:[0-9]+[a-zA-Z]* [a-zA-Z0-9]*|[a-zA-Z0-9]* [0-9]+[a-zA-Z]*), (?:[0-9]+[a-zA-Z]* [a-zA-Z0-9]*, |[a-zA-Z0-9]* [0-9]+[a-zA-Z]*, |)[A-Z][a-z]+'
        pattern = re.compile(reg_str) #用自己参照题目规范里德国地址和谷歌到的欧洲地址格式写的正则
        res = re.findall(pattern, input)
        if(len(res)>0):
            output = res[0]
            sensitive_words += " "
            sensitive_words += output
            find_sign = 1
        #都没找到，说明没有敏感元素
        if(find_sign==0):
            print("no sensitive element in:", input)
            output = "nothing"
        return sensitive_words

    #价格估计函数 根据历史交易记录来为数据估价
    def price_evaluaion(self):
        #输入size和accuracy
        Int, ok = QInputDialog.getInt(self, 'Input Info', 'Input size here (KB)', 1024, 1, 10000000)
        if(ok):
            this_size = Int
        Float, ok = QInputDialog.getDouble(self, 'Input Info', 'Input accuracy here (0~1)', 0.8, 0, 1, 2)
        if(ok):
            this_accuracy = Float
        #读取并构造数据
        history_price_datas = pd.read_csv('./datas/history_price.csv') 
        x = history_price_datas.iloc[:, 0:2].values 
        y = history_price_datas.iloc[:, 2].values
        x_test = [[this_size, this_accuracy]]
        #训练模型得到结果
        lin = LinearRegression() 
        lin.fit(x, y)
        y_pred = lin.predict(x_test)
        QMessageBox.information(self, "notion", "Predicated price is " + str(y_pred))
        

    #模型处理部分函数*********************************************************************************************************************

    #将联邦学习数据(文件的位置)上传至modelsets表
    def model_upload(self):
        #获取jobname
        jobname = self.lineedit_jobname.text()
        if(jobname == ""):
            QMessageBox.warning(self, "warning", "Please enter jobname")
            return 1
        #获取联邦学习模式
        model_mode = self.model_mode_choose
        #获取文件位置
        fname = QFileDialog.getOpenFileName(self, 'Openning File','./')
        if(fname[0] and ((('.txt' in fname[0])) or ('.csv' in fname[0]))):
            file_path = fname[0]
        else:
            QMessageBox.warning(self, "warning", "unsupported format!")
            return 1
        #将数据文件位置与记录上传到modelsets表
        rows = ['jobname', 'model_mode', 'file_path', 'seller_id']
        values = [jobname, model_mode, file_path, self.seller_id]
        db_add_one_row('modelsets', rows, values)
        QMessageBox.information(self, "notion", "successfully upload!")

    #选择联邦模型的模式
    def bt_group_clicked(self): 
        if self.bt_group.checkedId() == 1:
                self.model_mode_choose = "vertical"
        else:
            self.model_mode_choose = "horizonal"
        print(self.model_mode_choose)
    
    #数据查询部分函数*********************************************************************************************************************

    #将数据信息上传入库，同时更新querysets表
    def queryset_upload(self):
        #获取名字与价格
        name = self.lineedit_queryset_name.text()
        price = self.lineedit_query_price.text()
        if name == "":
            QMessageBox.warning(self, "warning", "Please enter name!")
            return 1
        if price == "":
            QMessageBox.warning(self, "warning", "Please enter price!")
            return 1
        self.lineedit_queryset_name.setText("")
        self.lineedit_query_price.setText("")
        #上传文件生成列表
        self.format_header, self.format_lines, fname = self.upload_file_into_lines(split_str = " ") #这里记得要分割
        self.format_lines = self.align_lines(self.format_lines) #要显示上表格，需要对齐！！！！
        print("header=",self.format_header,"\nlines=",self.format_lines)
        #基于表名、列名、类型创建表
        create_table_name = name
        create_table_rows = self.format_header
        create_table_rows_kinds = ['VARCHAR(50)'] * len(self.format_header) #目前每列的类型都是VARCHAR(50)
        db_create_table(create_table_name, create_table_rows, create_table_rows_kinds)
        #向表中新增大量数据
        insert_table_name = name
        insert_table_rows = self.format_header
        print("ready")
        for i in range(len(self.format_lines)):
            db_add_one_row_with_prefix(insert_table_name, insert_table_rows, self.format_lines[i], row_prefix='row_')
        print("done")
        #更新querysets表
        update_table_name = 'querysets'
        update_table_rows = ['name', 'price', 'seller']
        update_table_values = [name, price, self.seller_id]
        db_add_one_row(update_table_name, update_table_rows, update_table_values)
        #同时更新表格显示和表格标题 
        self.table_alldatas.setColumnCount(len(self.format_header))
        self.table_alldatas.setHorizontalHeaderLabels(self.format_header)
        self.flash_table_datas_from_format_lines(self.table_alldatas, self.format_lines)
        self.current_ontable_dataset = str(name)
        self.label_table_alldatas.setText("Current ontable set is: " + str(self.current_ontable_dataset))


    #其他通用处理部分函数******************************************************************************************************************

    #根据按格式排列的lines更新顶部数据显示表格
    def flash_table_datas_from_format_lines(self, TableWidget, datas, dimension=2):
        TableWidget.setRowCount(len(datas))
        if(dimension==2):
            for i in range(len(datas)):
                for j in range(len(datas[0])):
                    TableWidget.setItem(i, j, QTableWidgetItem(datas[i][j]))
        elif(dimension==1):
            for i in range(len(datas)):
                    TableWidget.setItem(i, 0, QTableWidgetItem(datas[i]))

    #上传文件成为列表
    def upload_file_into_lines(self, split_str=None):
        fname = QFileDialog.getOpenFileName(self, 'Openning File','./')
        format_lines = []
        format_header = []
        if fname[0]:
            #如果是.csv文件，就认为是有表头的，如果是.txt文件，就认为是没表头的，自动生成表头
            if (".txt" in fname[0]):
                with open(fname[0], 'r',encoding='gb18030',errors='ignore') as f:   
                    flines = f.read().splitlines()
                    for line in flines:
                        if(split_str==None):
                            format_line = line
                        elif(split_str==" "):
                            format_line = line.split()
                        else:
                            format_line = line.strip().split(split_str)
                        format_lines.append(format_line)
                    #自动按数字生成表头
                    if(split_str==None):
                        format_header=['0']
                    else:
                        for i in range(0,len(format_lines[0])): #自动按数字生成表头
                            format_header.append(str(i))
            elif (".csv" in fname[0]):
                with open(fname[0], 'r', errors='ignore') as f: 
                #with open(fname[0], 'r',encoding='gb18030',errors='ignore') as f:   
                    flines = f.read().splitlines()
                    for i in range(len(flines)):
                        if i == 0:
                            if(split_str==None):
                                format_header = flines[0]
                            elif(split_str==" "):
                                format_header = flines[0].split() 
                            else:
                                format_header = flines[0].strip().split(split_str) 
                        else:
                            if(split_str==None):
                                format_line = flines[i]
                            elif(split_str==" "):
                                format_line = flines[i].split() 
                            else:
                                format_line = flines[i].strip().split(split_str)
                            format_lines.append(format_line)   
            else:
                QMessageBox.warning(self, "warning", "unsupported format!")
        return format_header, format_lines, fname[0]
    
    #将format_lines中每行字段内容长度对齐
    def align_lines(self, lines):
        max_len = len(lines[0])
        for line in lines:
            if(len(line) > max_len):
                max_len = len(line)
        for i in range(len(lines)):
            for j in range(len(lines[i]), max_len):
                lines[i].append("") #用空字符串来填充
        return lines