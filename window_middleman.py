#coding = 'utf-8'

from database_funs import * #数据库有关操作函数
from vertical_federated_learning import *  #垂直联邦学习有关函数
from horizonal_federated_learning import *  #水平联邦学习有关函数

from PyQt5.QtWidgets import QPlainTextEdit, QFileDialog, QButtonGroup, QInputDialog, QLabel, QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QMessageBox, QTableWidget, QAction, QTableWidgetItem, QRadioButton
from PyQt5.QtGui import QFont, QPalette, QPixmap, QBrush, QIcon
from PyQt5.QtCore import Qt
from PyQt5.Qt import *
import pandas as pd
import numpy as np

#文件路径大合集
ICON_PATH = './images/bg_son.jpg'
WELCOME_BG_PATH = "./images/bg_son.jpg"

##中间商界面################################################################################################################################
class Window_Middleman_Main(QDialog):
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
        self.middleman_id = None
        self.current_ontable = 'None'
        #设置该窗口元素
        self.Init_UI()

    def Init_UI(self):
        #窗口设置
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT) 
        self.setWindowTitle('MiniDTM_Middleman')
        self.setWindowIcon(QIcon(ICON_PATH))
        #背景图片
        palette = QPalette()
        pix=QPixmap(WELCOME_BG_PATH)
        pix = pix.scaled(self.width(),self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        #顶部综合显示框
        self.label_table_alldatas = QLabel(self)
        self.label_table_alldatas.setText("Current ontable  is: " + str(self.current_ontable))
        self.label_table_alldatas.setStyleSheet("color: cornsilk")
        self.label_table_alldatas.setAlignment(Qt.AlignCenter)
        font_label_table_alldatas = QFont()
        font_label_table_alldatas.setPointSize(12)
        font_label_table_alldatas.setBold(True)
        self.label_table_alldatas.setFont(font_label_table_alldatas)
        self.table_alldatas = QTableWidget(self)
        #1 原始数据集-数据包部分
        #标题
        self.label_integrate2pkg = QLabel(self)
        self.label_integrate2pkg.setText("Intergrate Rawdatas to Datapkgs")
        self.label_integrate2pkg.setStyleSheet("color: cornsilk")
        self.label_integrate2pkg.setAlignment(Qt.AlignCenter)
        font_label_integrate2pkg = QFont()
        font_label_integrate2pkg.setPointSize(12)
        font_label_integrate2pkg.setBold(True)
        self.label_integrate2pkg.setFont(font_label_integrate2pkg)
        #输入框与按钮
        self.bt_show_rawdatas = QPushButton('Show Rawdatas', self)
        self.bt_show_rawdatas.clicked.connect(self.show_rawdatas)
        self.bt_integrate2pkg = QPushButton('Intergrate Rawdatas', self)
        self.bt_integrate2pkg.clicked.connect(self.integrate2pkg)
        #2 模型训练部分
        #标题
        self.label_federated_learning = QLabel(self)
        self.label_federated_learning.setText("Federated_Learning")
        self.label_federated_learning.setStyleSheet("color: cornsilk")
        self.label_federated_learning.setAlignment(Qt.AlignCenter)
        font_label_federated_learning = QFont()
        font_label_federated_learning.setPointSize(12)
        font_label_federated_learning.setBold(True)
        self.label_federated_learning.setFont(font_label_federated_learning)
        #输入框与按钮
        self.bt_show_modelsets = QPushButton('Show Modelsets', self)
        self.bt_show_modelsets.clicked.connect(self.show_modelsets)
        self.bt_horizontal_federated_learning = QPushButton('Horizontal Federated Learning', self)
        self.bt_horizontal_federated_learning.clicked.connect(self.horizontal_federated_learning)
        self.bt_vertical_federated_learning = QPushButton('Vertical Federated Learning', self)
        self.bt_vertical_federated_learning.clicked.connect(self.vertical_federated_learning)
        #3 数据查询部分
        #标题
        self.label_query = QLabel(self)
        self.label_query.setText("Data Query")
        self.label_query.setStyleSheet("color: cornsilk")
        self.label_query.setAlignment(Qt.AlignCenter)
        font_label_query = QFont()
        font_label_query.setPointSize(12)
        font_label_query.setBold(True)
        self.label_query.setFont(font_label_query)
        #输入框与按钮
        self.bt_show_querysets = QPushButton('Show Querysets', self)
        self.bt_show_querysets.clicked.connect(self.show_querysets)
        self.lineedit_queryset_name = QLineEdit(self)
        self.lineedit_queryset_name.setPlaceholderText("input queryset name here")
        self.lineedit_queryset_condition = QLineEdit(self)
        self.lineedit_queryset_condition.setPlaceholderText("input fliter condition here")
        self.bt_query = QPushButton('Query', self)
        self.bt_query.clicked.connect(self.query_datas)
        self.bt_release_dataservice = QPushButton('Release', self)
        self.bt_release_dataservice.clicked.connect(self.release_dataservice)
        #4 竞价处理部分
        #标题
        self.label_biddings = QLabel(self)
        self.label_biddings.setText("Biddings")
        self.label_biddings.setStyleSheet("color: cornsilk")
        self.label_biddings.setAlignment(Qt.AlignCenter)
        font_label_biddings = QFont()
        font_label_biddings.setPointSize(12)
        font_label_biddings.setBold(True)
        self.label_biddings.setFont(font_label_biddings)
        #输入框与按钮
        self.bt_show_biddings = QPushButton('Show Biddings', self)
        self.bt_show_biddings.clicked.connect(self.show_biddings)
        self.lineedit_datapkg_id = QLineEdit(self)
        self.lineedit_datapkg_id.setPlaceholderText("input bidding datapkg id")
        self.bt_dealing_bidding = QPushButton('Deal With Bidding', self)
        self.bt_dealing_bidding.clicked.connect(self.dealing_bidding)
        #显示布局设置
        vbox = QVBoxLayout()
        #0 顶部综合框
        vbox.addWidget(self.label_table_alldatas)
        vbox.addWidget(self.table_alldatas)
        #1 原始数据区
        vbox.addWidget(self.label_integrate2pkg)
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.bt_show_rawdatas)
        hbox1.addWidget(self.bt_integrate2pkg)
        hbox1.addStretch(1)
        vbox.addLayout(hbox1)
        #2 模型训练区
        vbox.addWidget(self.label_federated_learning)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.bt_show_modelsets)
        hbox2.addWidget(self.bt_horizontal_federated_learning)
        hbox2.addWidget(self.bt_vertical_federated_learning)
        hbox2.addStretch(1)
        vbox.addLayout(hbox2)
        #3 数据查询部分
        vbox.addWidget(self.label_query)
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.bt_show_querysets)
        hbox3.addWidget(self.lineedit_queryset_name)
        hbox3.addWidget(self.lineedit_queryset_condition)
        hbox3.addWidget(self.bt_query)
        hbox3.addWidget(self.bt_release_dataservice)
        hbox3.addStretch(1)
        vbox.addLayout(hbox3)
        #4 竞价处理部分
        vbox.addWidget(self.label_biddings)
        hbox4 = QHBoxLayout()
        hbox4.addStretch(1)
        hbox4.addWidget(self.bt_show_biddings)
        hbox4.addWidget(self.lineedit_datapkg_id)
        hbox4.addWidget(self.bt_dealing_bidding)
        hbox4.addStretch(1)
        vbox.addLayout(hbox4)
        #完成
        self.setLayout(vbox)
        self.show()
    
    #整合数据集打包部分函数*****************************************************************************************************************
    
    #表格显示原始数据集
    def show_rawdatas(self):
        cols = db_get_col_list('rawdatas') #设置列
        self.table_alldatas.setColumnCount(len(cols)) 
        self.table_alldatas.setHorizontalHeaderLabels(cols[:len(cols)]) #设置表头
        datas = db_get_table_datas('rawdatas') #设置行
        self.flash_table_datas(self.table_alldatas, datas) #根据取得的数据刷新表中内容
        self.current_ontable = 'rawdatas'

    #整合原始数据集为数据包，并进行区分定价发布
    def integrate2pkg(self):
        #弹窗填写数据集名，若有多个则以;来分割
        text, ok = QInputDialog.getText(self, 'Input Rawdatas Name', 'Divided by ;')
        if(ok):
            if(text==''): #如果为空
                QMessageBox.warning(self, "warning", "No input!")
                return 1
            else:
                rawdatas_list = text.split(";")
        print(rawdatas_list)
        #确保数据库中有所输入的数据集名
        all_names = []
        datas = db_get_table_datas('rawdatas')
        for item in datas:
            all_names.append(item['name'])
        for name in rawdatas_list:
            if(name not in all_names):
                QMessageBox.warning(self, "warning", "rawdatas not found!")
                return 1
        #弹窗命名数据包，输入整合后size和accuracy
        #输入完整数据集定价，然后自动生成n份出价
        #发布，同步到数据库
        #为避免反复弹窗，这些全部在子窗口中完成
        window_middleman_sub = Window_Middleman_Sub()
        window_middleman_sub.middleman_id = self.middleman_id
        window_middleman_sub.exec()
        
    #模型训练部分函数*****************************************************************************************************************
    
    #表格显示训练数据
    def show_modelsets(self):
        cols = db_get_col_list('modelsets') #设置列
        self.table_alldatas.setColumnCount(len(cols)) 
        self.table_alldatas.setHorizontalHeaderLabels(cols[:len(cols)]) #设置表头
        datas = db_get_table_datas('modelsets') #设置行
        self.flash_table_datas(self.table_alldatas, datas) #根据取得的数据刷新表中内容
        self.current_ontable = 'modelsets'

    #垂直联邦学习
    def vertical_federated_learning(self):
        #获取文件路径
        res = db_get_table_datas_with_constraint('modelsets','model_mode = \'vertical\'')
        file_list = []
        for item in res:
            file_list.append(item['file_path'])
        #启动垂直联邦学习
        learning_result = fun_vertical_federated_learning(file_list)
        #显示结果
        QMessageBox.information(self, "Learning Completed!", "The final model accuracy is "+str(learning_result))

    #水平联邦学习
    def horizontal_federated_learning(self):
        #获取文件路径
        res = db_get_table_datas_with_constraint('modelsets','model_mode = \'horizonal\'')
        file_list = []
        for item in res:
            file_list.append(item['file_path'])
        print("file_list=",file_list)
        #启动水平联邦学习
        final_score, real_contribution = horizontal_federated_learning(file_list)
        print('done')
        #显示结果
        showcase_str = 'The final score is ' + str(final_score) + '. '
        for i in range(len(real_contribution)):
            showcase_str += 'The contribution of member ' + str(i) + ' is ' + str(real_contribution[i]) + '. '
        QMessageBox.information(self, "Learning Completed!", showcase_str)


    #数据查询部分函数*****************************************************************************************************************

    #表格显示训练数据
    def show_querysets(self):
        cols = db_get_col_list('querysets') #设置列
        self.table_alldatas.setColumnCount(len(cols)) 
        self.table_alldatas.setHorizontalHeaderLabels(cols[:len(cols)]) #设置表头
        datas = db_get_table_datas('querysets') #设置行
        self.flash_table_datas(self.table_alldatas, datas) #根据取得的数据刷新表中内容
        self.current_ontable = 'querysets'

    #数据查询服务函数
    def query_datas(self):
        #获取并检查输入
        queryset_name = self.lineedit_queryset_name.text()
        queryset_condition = self.lineedit_queryset_condition.text()
        if(queryset_name=='' or queryset_condition==''):
            QMessageBox.warning(self, "warning", "Incomplete Input!")
            return 1
        #从db中获取数据
        self.query_result = db_get_table_datas_with_constraint(queryset_name, queryset_condition)
        #弹窗提示价格
        info = db_get_table_datas_with_constraint('querysets', 'name = \'' + queryset_name + '\'')
        price = int(info[0]['price']) * len(self.query_result)
        QMessageBox.warning(self, "warning", "This Query Service Need "+str(price)+'!')
        #显示到表上
        cols = db_get_col_list(queryset_name) #设置列
        self.table_alldatas.setColumnCount(len(cols)) 
        self.table_alldatas.setHorizontalHeaderLabels(cols[:len(cols)]) 
        self.flash_table_datas(self.table_alldatas, self.query_result) #根据取得的数据刷新表中内容
    
    #将查询到的数据发布成产品，弹窗输入产品信息
    def release_dataservice(self):
        if(len(self.query_result) < 1):
            QMessageBox.warning(self, "warning", "No query info!")
            return 1
        #弹窗输入价格
        Float, ok = QInputDialog.getDouble(self, 'Input Info', 'Input price here (0~1)', 0.8, 0, 1, 2)
        if(ok):
            price = Float
        #发布到数据库
        row_list = ['price', 'middleman']
        value_list = [str(price), self.middleman_id]
        db_add_one_row('market_dataservice', row_list, value_list)
        QMessageBox.information(self, "notion", 'successfully released!')

        
    #处理拍卖竞价部分函数*****************************************************************************************************************

    #表格显示竞价数据
    def show_biddings(self):
        cols = db_get_col_list('bidding') #设置列
        self.table_alldatas.setColumnCount(len(cols)) 
        self.table_alldatas.setHorizontalHeaderLabels(cols[:len(cols)]) #设置表头
        datas = db_get_table_datas('bidding') #设置行
        self.flash_table_datas(self.table_alldatas, datas) #根据取得的数据刷新表中内容
        self.current_ontable = 'bidding'

    #处理竞价
    def dealing_bidding(self):
        #获取并检查输入
        datapkg_id = self.lineedit_datapkg_id.text()
        if(datapkg_id==''):
            QMessageBox.warning(self, "warning", "Incomplete Input!")
            return 1
        #弹窗输入保留阈值
        Int, ok = QInputDialog.getInt(self, 'Input Info', 'Input reserve bar', 1024, 1, 10000000)
        if(ok):
            reserve_bar = Int
        #获取所有的出价
        bidding_result = db_get_table_datas_with_constraint('bidding','datapkg_id = '+datapkg_id)
        #判断是否达到条件
        price_list = []
        for i in range(len(bidding_result)):
            price_list.append(bidding_result[i]['price'])
        max2 = np.sort(price_list)[-2]
        max1 = np.sort(price_list)[-1]
        if(max2>max1-reserve_bar): #达到条件，将产品卖出
            #在market_datapkg中清除商品
            db = connect2db()
            cursor = db.cursor()
            sql = 'delete from market_dataproduct where id = %s' % datapkg_id
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            print("qing chu cheng gong")
            #在history中加入记录
            for i in range(len(bidding_result)):
                if(bidding_result[i]['price'] == max2):
                    buyer = bidding_result[i]['buyer_id']
            row_list = ['name', 'price', 'buyer', 'middleman'] #name这列用datapkg_id代替
            value_list = [datapkg_id, str(max2), buyer, self.middleman_id]
            db_add_one_row('history', row_list, value_list)
            print("tian jia cheng gong")
            #弹窗提示拍卖成功，成交价与拍得者
            QMessageBox.information(self, "notion", 'successfully sold! buyer is '+buyer+', price is '+str(max2))
        else: #未到条件，在market_datapkg中更新last_price
            db = connect2db()
            cursor = db.cursor()
            sql = 'update market_datapkg set lastprice = ' + str(max1-reserve_bar) + ' where id = \'' + datapkg_id +'\''
            print("sql=",sql)
            cursor.execute(sql)
            print('success')
            db.commit()
            cursor.close()
            db.close()
            #弹窗提示拍卖未成功
            QMessageBox.information(self, "notion", 'bidding failed. Last price is ' + str(max1-reserve_bar))
        #无论有没有卖出，都在bidding中清除出价记录
        db = connect2db()
        cursor = db.cursor()
        sql = 'delete from bidding where datapkg_id = \'' + datapkg_id +'\''
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        print("all done")
        #还要刷新表格显示
        self.show_biddings()

    #其他通用处理部分函数******************************************************************************************************************

    #来自buyer
    # 根据表头，自动从全表数据中截取所需字段显示在表上
    def flash_table_datas(self, TableWidget, datas):
        TableWidget.setRowCount(len(datas))
        attributes = []
        for i in range(TableWidget.columnCount()):
            attributes.append(TableWidget.horizontalHeaderItem(i).text())
        for i in range(len(datas)):
            pos = 0
            for attribute in attributes:
                TableWidget.setItem(i,pos,QTableWidgetItem(str(datas[i][attribute])))  
                pos += 1 

    #来自seller
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


##发布datapkg页面###########################################################################################################################
class Window_Middleman_Sub(QDialog):
    def __init__(self):
        super().__init__()
        #获取屏幕分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        #设置窗口大小
        self.HEIGHT = int(self.screenRect.height() * 0.4)
        self.WIDTH = int(self.screenRect.width() * 0.4)
        self.TOP = int(self.screenRect.height() * 0.3)
        self.LEFT = int(self.screenRect.width() * 0.3)
        #从上一级窗口继承的变量
        self.middleman_id = None
        #设置该窗口元素
        self.Init_UI()

    def Init_UI(self):
        #窗口设置
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT) 
        self.setWindowTitle('MiniDTM_Middleman_ReleasePkgs')
        self.setWindowIcon(QIcon(ICON_PATH))
        #背景图片
        palette = QPalette()
        pix=QPixmap(WELCOME_BG_PATH)
        pix = pix.scaled(self.width(),self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        #name、accuracy、size、price、partition输入框，生成按钮
        self.lineedit_name = QLineEdit(self)
        self.lineedit_name.setPlaceholderText("input name here")
        self.lineedit_accuracy = QLineEdit(self)
        self.lineedit_accuracy.setPlaceholderText("input accuracy here")
        self.lineedit_size = QLineEdit(self)
        self.lineedit_size.setPlaceholderText("input size here")
        self.lineedit_price = QLineEdit(self)
        self.lineedit_price.setPlaceholderText("input price here")
        self.lineedit_partition = QLineEdit(self)
        self.lineedit_partition.setPlaceholderText("input partition here")
        self.bt_divide = QPushButton("Divide into sub pkgs", self)
        self.bt_divide.clicked.connect(self.divide_datapkg)
        #显示拆分结果与确定发布按钮
        self.lineedit_part1 = QLineEdit(self)
        self.lineedit_part2 = QLineEdit(self)
        self.lineedit_part3 = QLineEdit(self)
        self.lineedit_part4 = QLineEdit(self)
        self.lineedit_part5 = QLineEdit(self)
        self.bt_release_pkgs = QPushButton("Release Packages", self)
        self.bt_release_pkgs.clicked.connect(self.release_pkgs)
        #显示布局
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.lineedit_name)
        hbox1.addWidget(self.lineedit_accuracy)
        hbox1.addWidget(self.lineedit_size)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.lineedit_price)
        hbox2.addWidget(self.lineedit_partition)
        hbox2.addWidget(self.bt_divide)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.lineedit_part1)
        vbox.addWidget(self.lineedit_part2)
        vbox.addWidget(self.lineedit_part3)
        vbox.addWidget(self.lineedit_part4)
        vbox.addWidget(self.lineedit_part5)
        vbox.addWidget(self.bt_release_pkgs)
        self.setLayout(vbox)
        self.show()
    
    #自动拆分成小份的
    def divide_datapkg(self):
        #检查输入
        self.lineedit_list = [self.lineedit_name, self.lineedit_accuracy, self.lineedit_size, self.lineedit_price, self.lineedit_partition]
        for lineedit in self.lineedit_list:
            if lineedit.text() == '':
                QMessageBox.warning(self, "warning", "invalid input")
                return 1
        #生成分布
        self.partition = []
        for i in range(0, min(int(self.lineedit_partition.text()), 5)): #最多生成5组
            accuracy = np.random.random() * float(self.lineedit_accuracy.text())
            size = np.random.random() * int(self.lineedit_accuracy.text())
            how_big = (size*accuracy) / (int(self.lineedit_accuracy.text())*float(self.lineedit_accuracy.text()))
            balance = -0.25*pow(how_big,2) + 2*how_big +0.25
            price = (  balance * float(self.lineedit_price.text()) )
            item = {'accuracy':accuracy, 'size':size, 'price':price}
            self.partition.append(item)
        #显示分布
        self.lineedit_partition_list = [self.lineedit_part1, self.lineedit_part2, self.lineedit_part3, self.lineedit_part4, self.lineedit_part5]
        for i in range(len(self.lineedit_partition_list)):
            self.lineedit_partition_list[i].setText('accuracy:'+str(self.partition[i]['accuracy'])+' size:'+str(self.partition[i]['size'])+' price:'+str(self.partition[i]['price']))
        
    #发布数据包们
    def release_pkgs(self):
        row_list = ['name', 'size', 'accuracy', 'lastprice']
        for i in range(len(self.lineedit_partition_list)):
            valuelist = [str(self.lineedit_name.text())+'_'+str(i), str(self.partition[i]['size']), str(self.partition[i]['accuracy']), str(self.partition[i]['price'])]
            db_add_one_row('market_datapkg', row_list, valuelist)
        print("release success")
        self.close()