#coding = 'utf-8'

from database_funs import * #数据库有关操作函数

import sys
from PyQt5.QtWidgets import (QInputDialog, QLabel, QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QMessageBox, QTableWidget, QAction, QTableWidgetItem)
from PyQt5.QtGui import QFont, QPalette, QPixmap, QBrush, QIcon
from PyQt5.QtCore import Qt
from PyQt5.Qt import *
import re

#文件路径大合集
ICON_PATH = './images/bg_son.jpg'
WELCOME_BG_PATH = "./images/bg_son.jpg"

##买家界面##################################################################################################################################
class Window_Buyer_Main(QDialog):
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
        self.buyer_id = None
        #设置该窗口元素
        self.Init_UI()

    def Init_UI(self):
        #窗口设置
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT) 
        self.setWindowTitle('MiniDTM_Buyers')
        self.setWindowIcon(QIcon(ICON_PATH))
        #背景图片
        palette = QPalette()
        pix=QPixmap(WELCOME_BG_PATH)
        pix = pix.scaled(self.width(),self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        #市场数据包表
        self.label_table_datapkg = QLabel(self)
        self.label_table_datapkg.setText("Data Packages")
        self.label_table_datapkg.setStyleSheet("color: cornsilk")
        self.label_table_datapkg.setAlignment(Qt.AlignCenter)
        font_label_table_datapkg = QFont()
        font_label_table_datapkg.setPointSize(12)
        font_label_table_datapkg.setBold(True)
        self.label_table_datapkg.setFont(font_label_table_datapkg)
        self.table_datapkg = QTableWidget(self)
        self.table_datapkg_cols = db_get_col_list('market_datapkg') #设置列
        self.table_datapkg.setColumnCount(len(self.table_datapkg_cols)) 
        self.table_datapkg.setHorizontalHeaderLabels(self.table_datapkg_cols[:len(self.table_datapkg_cols)]) 
        self.table_datapkg_datas = db_get_table_datas('market_datapkg') #设置行
        self.flash_table_datas(self.table_datapkg, self.table_datapkg_datas) #根据取得的数据刷新表中内容
        #市场数据产品表
        self.label_table_product = QLabel(self)
        self.label_table_product.setText("Data Products")
        self.label_table_product.setStyleSheet("color: cornsilk")
        self.label_table_product.setAlignment(Qt.AlignCenter)
        font_label_table_product = QFont()
        font_label_table_product.setPointSize(12)
        font_label_table_product.setBold(True)
        self.label_table_product.setFont(font_label_table_product)
        self.table_product = QTableWidget(self)
        self.table_product_cols = db_get_col_list('market_dataproduct') #设置列
        self.table_product.setColumnCount(len(self.table_product_cols)) 
        self.table_product.setHorizontalHeaderLabels(self.table_product_cols[:len(self.table_product_cols)]) 
        self.table_product_datas = db_get_table_datas('market_dataproduct') #设置行
        self.flash_table_datas(self.table_product, self.table_product_datas) #根据取得的数据刷新表中内容
        #市场数据服务表
        self.label_table_service = QLabel(self)
        self.label_table_service.setText("Data Services")
        self.label_table_service.setStyleSheet("color: cornsilk")
        self.label_table_service.setAlignment(Qt.AlignCenter)
        font_label_table_service = QFont()
        font_label_table_service.setPointSize(12)
        font_label_table_service.setBold(True)
        self.label_table_service.setFont(font_label_table_service)
        self.table_service = QTableWidget(self)
        self.table_service_cols = db_get_col_list('market_dataservice') #设置列
        self.table_service.setColumnCount(len(self.table_service_cols)) 
        self.table_service.setHorizontalHeaderLabels(self.table_service_cols[:len(self.table_service_cols)]) 
        self.table_service_datas = db_get_table_datas('market_dataservice') #设置行
        self.flash_table_datas(self.table_service, self.table_service_datas) #根据取得的数据刷新表中内容
        #双击表格绑定函数
        self.table_datapkg.doubleClicked.connect(self.table_double_clicked)
        self.table_product.doubleClicked.connect(self.table_double_clicked)
        self.table_service.doubleClicked.connect(self.table_double_clicked)
        #按钮
        self.bt_datapkg_filter_size = QPushButton('filter for size', self)
        self.bt_datapkg_filter_price = QPushButton('filter for price', self)
        self.bt_dataproduct_filter_accuracy = QPushButton('filter for accuracy', self)
        self.bt_dataproduct_filter_price = QPushButton('filter for price', self)
        self.bt_dataservice_filter_price = QPushButton('filter for price', self)
        self.bt_datapkg_filter_size.clicked.connect(self.bt_clicked)
        self.bt_datapkg_filter_price.clicked.connect(self.bt_clicked)
        self.bt_dataproduct_filter_accuracy.clicked.connect(self.bt_clicked)
        self.bt_dataproduct_filter_price.clicked.connect(self.bt_clicked)
        self.bt_dataservice_filter_price.clicked.connect(self.bt_clicked)
        #筛选条件输入框
        self.filter_input_datapkg = QLineEdit(self)
        self.filter_input_dataproduct = QLineEdit(self)
        self.filter_input_dataservice = QLineEdit(self)
        self.filter_input_datapkg.setPlaceholderText("input filter constraints here eg.price<100")
        self.filter_input_dataproduct.setPlaceholderText("input filter constraints here eg.price<100")
        self.filter_input_dataservice.setPlaceholderText("input filter constraints here eg.price<100")
        #设置画面布局
        Vbox = QVBoxLayout()
        Vbox.addWidget(self.label_table_datapkg) #第一个表格标题
        Vbox.addWidget(self.table_datapkg) 
        Hbox1 = QHBoxLayout() #第一个表格右下角按钮
        Hbox1.addStretch(1)
        Hbox1.addWidget(self.filter_input_datapkg)
        Hbox1.addWidget(self.bt_datapkg_filter_size)
        Hbox1.addWidget(self.bt_datapkg_filter_price)
        Vbox.addLayout(Hbox1)
        Vbox.addWidget(self.label_table_product) #第二个表格标题
        Vbox.addWidget(self.table_product) 
        Hbox2 = QHBoxLayout() #第二个表格右下角按钮
        Hbox2.addStretch(1)
        Hbox2.addWidget(self.filter_input_dataproduct)
        Hbox2.addWidget(self.bt_dataproduct_filter_accuracy)
        Hbox2.addWidget(self.bt_dataproduct_filter_price)
        Vbox.addLayout(Hbox2)
        Vbox.addWidget(self.label_table_service) #第三个表格标题
        Vbox.addWidget(self.table_service)
        Hbox3 = QHBoxLayout() #第三个表格右下角按钮
        Hbox3.addStretch(1)
        Hbox3.addWidget(self.filter_input_dataservice)
        Hbox3.addWidget(self.bt_dataservice_filter_price)
        Vbox.addLayout(Hbox3)
        self.setLayout(Vbox) #布局完成
        self.show()

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
    
    # 双击表格，启动拍卖或购买
    def table_double_clicked(self):
            sender = self.sender()
            #双击了数据包表
            if(sender == self.table_datapkg): 
                print("table_datapkg")
                #打印被选中的单元格
                for selected in self.sender().selectedItems():
                    print(selected.row(), selected.column(), selected.text())
                #启动出价窗口
                self.window_buyer_bid = Window_Buyer_Bid()
                #传递选中的数据包名称给出价窗口
                for i in range(self.table_datapkg.columnCount()): #找到name字段的位置
                    if(self.table_datapkg.horizontalHeaderItem(i).text()=='name'):
                        name_pos = i
                        break
                self.window_buyer_bid.bid_target_name = self.table_datapkg.item(selected.row(), name_pos).text() 
                self.window_buyer_bid.label_notion.setText("You are bidding for: " + self.window_buyer_bid.bid_target_name)
                #传递选中的数据包的ID给出价窗口
                for i in range(self.table_datapkg.columnCount()): #找到name字段的位置
                    if(self.table_datapkg.horizontalHeaderItem(i).text()=='id'):
                        id_pos = i
                        break
                self.window_buyer_bid.bid_datapkg_id = self.table_datapkg.item(selected.row(), id_pos).text() 
                #传递买家ID
                self.window_buyer_bid.buyer_id = self.buyer_id
                #启动
                self.window_buyer_bid.exec()
            #双击了数据产品表
            elif(sender == self.table_product):
                #打印被选中的单元格
                for selected in self.sender().selectedItems():
                    print(selected.row(), selected.column(), selected.text())
                #找到该对象价格
                for i in range(self.table_product.columnCount()): #找到price字段的位置
                    if(self.table_product.horizontalHeaderItem(i).text()=='price'):
                        price_pos = i
                        break
                this_price = self.table_product.item(selected.row(), price_pos).text() 
                #找到该对象name
                for i in range(self.table_product.columnCount()): #找到name字段的位置
                    if(self.table_product.horizontalHeaderItem(i).text()=='name'):
                        name_pos = i
                        break
                this_name = self.table_product.item(selected.row(), name_pos).text() 
                #找到该对象id
                for i in range(self.table_product.columnCount()): #找到name字段的位置
                    if(self.table_product.horizontalHeaderItem(i).text()=='id'):
                        id_pos = i
                        break
                this_id = self.table_product.item(selected.row(), id_pos).text() 
                #找到该对象的中间商
                for i in range(self.table_product.columnCount()): #找到middleman字段的位置
                    if(self.table_product.horizontalHeaderItem(i).text()=='middleman'):
                        middleman_pos = i
                        break
                this_middleman = self.table_product.item(selected.row(), middleman_pos).text() 
                #启动一口价购买
                reply = QMessageBox.information(self,'caution','are you sure to buy this product with the price of ' + this_price, QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
                if reply == QMessageBox.Ok:
                    QMessageBox.warning(self, "notion", "sucessfully paid!")
                    #从数据市场表删去该产品，刷新表格显示
                    db = connect2db()
                    cursor = db.cursor()
                    sql = 'delete from market_dataproduct where id = %s' % this_id
                    print("sql=", sql)
                    cursor.execute(sql)
                    db.commit()
                    cursor.close()
                    print('delete done')
                    new_datas = db_get_table_datas('market_dataproduct') #设置行
                    self.flash_table_datas(self.table_product, new_datas) #根据取得的数据刷新表中内容
                    print("flash done")
                    #将交易信息新增到平台交易记录中
                    cursor = db.cursor()
                    sql = 'insert into history(name, price, buyer, middleman) values(%s,%s,%s,%s);'
                    values = [this_name, this_price, self.buyer_id, this_middleman]
                    cursor.execute(sql, values)
                    db.commit()
                    cursor.close()
                    db.close()
                else:
                    QMessageBox.warning(self, "notion", "perchase abort")
            #双击数据服务表
            elif(sender == self.table_service):
                #打印被选中的单元格
                for selected in self.sender().selectedItems():
                    print(selected.row(), selected.column(), selected.text())
                #找到该对象价格
                for i in range(self.table_service.columnCount()): #找到price字段的位置
                    if(self.table_service.horizontalHeaderItem(i).text()=='price'):
                        price_pos = i
                        break
                this_price = self.table_service.item(selected.row(), price_pos).text() 
                #找到该对象name
                for i in range(self.table_service.columnCount()): #找到name字段的位置
                    if(self.table_service.horizontalHeaderItem(i).text()=='name'):
                        name_pos = i
                        break
                this_name = self.table_service.item(selected.row(), name_pos).text() 
                #找到该对象id
                for i in range(self.table_service.columnCount()): #找到id字段的位置
                    if(self.table_service.horizontalHeaderItem(i).text()=='id'):
                        id_pos = i
                        break
                this_id = self.table_service.item(selected.row(), id_pos).text() 
                #找到该对象的中间商
                for i in range(self.table_service.columnCount()): #找到middleman字段的位置
                    if(self.table_service.horizontalHeaderItem(i).text()=='middleman'):
                        middleman_pos = i
                        break
                this_middleman = self.table_service.item(selected.row(), middleman_pos).text() 
                #启动一口价购买
                reply = QMessageBox.information(self,'caution','are you sure to buy this service with the price of ' + this_price, QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
                if reply == QMessageBox.Ok:
                    QMessageBox.warning(self, "notion", "sucessfully paid!")
                    #从数据市场表删去该产品，刷新表格显示
                    db = connect2db()
                    cursor = db.cursor()
                    sql = 'delete from market_dataservice where id = %s' % this_id
                    cursor.execute(sql)
                    db.commit()
                    cursor.close()
                    db.close()
                    new_datas = db_get_table_datas('market_dataservice') #设置行
                    self.flash_table_datas(self.table_service, new_datas) #根据取得的数据刷新表中内容
                    print("flash done")
                    #将交易信息新增到平台交易记录中，(并进行还没有写的加密)
                    db = connect2db()
                    cursor = db.cursor()
                    sql = 'insert into history(name, price, buyer, middleman) values(%s,%s,%s,%s);'
                    values = [this_name, this_price, self.buyer_id, this_middleman]
                    cursor.execute(sql, values)
                    db.commit()
                    cursor.close()
                    db.close()
                else:
                    QMessageBox.warning(self, "notion", "perchase abort")
    
    #双击筛选按钮
    def bt_clicked(self):
        print("")
        sender = self.sender()
        if((sender == self.bt_datapkg_filter_size) or (sender == self.bt_datapkg_filter_price)):
            table_name = "market_datapkg"
            constraint = self.filter_input_datapkg.text()
            datas = db_get_table_datas_with_constraint(table_name, constraint)
            self.flash_table_datas(self.table_datapkg, datas)
        elif((sender == self.bt_dataproduct_filter_accuracy) or (sender == self.bt_dataproduct_filter_price)):
            table_name = "market_dataproduct"
            constraint = self.filter_input_dataproduct.text()
            datas = db_get_table_datas_with_constraint(table_name, constraint)
            self.flash_table_datas(self.table_product, datas)
        elif(sender == self.bt_dataservice_filter_price):
            table_name = "market_dataservice"
            constraint = self.filter_input_dataservice.text()
            datas = db_get_table_datas_with_constraint(table_name, constraint)
            self.flash_table_datas(self.table_service, datas)


##买家拍卖出价界面#############################################################################################################################
class Window_Buyer_Bid(QDialog):
    def __init__(self):
        super().__init__()
        #获取屏幕分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        #设置窗口大小
        self.HEIGHT = int(self.screenRect.height() * 0.2)
        self.WIDTH = int(self.screenRect.width() * 0.2)
        self.TOP = int(self.screenRect.height() * 0.4)
        self.LEFT = int(self.screenRect.width() * 0.4)
        #设置该窗口元素
        self.bid_target_name = "123"
        self.bid_datapkg_id = None
        self.buyer_id = None
        self.Init_UI()

    def Init_UI(self):
        #窗口设置
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT) 
        self.setWindowTitle('MiniDTM_Buyers')
        self.setWindowIcon(QIcon(ICON_PATH))
        #背景图片
        palette = QPalette()
        pix=QPixmap(WELCOME_BG_PATH)
        pix = pix.scaled(self.width(),self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        #提示标题
        self.label_notion = QLabel()
        self.label_notion.setText(self.bid_target_name)
        self.label_notion.setStyleSheet("color: red")
        self.label_notion.setAlignment(Qt.AlignCenter)
        font_label_notion = QFont()
        font_label_notion.setPointSize(12)
        font_label_notion.setBold(True)
        self.label_notion.setFont(font_label_notion)
        #金额输入框
        self.bid_input = QLineEdit(self)
        self.bid_input.setPlaceholderText("input price here")
        self.bid_input.setClearButtonEnabled(True)
        #出价按钮
        self.bt_bid = QPushButton("Bid", self)
        self.bt_bid.clicked.connect(self.bt_bid_clicked)
        #显示布局
        VBox = QVBoxLayout()
        VBox.addWidget(self.label_notion)
        VBox.addWidget(self.bid_input)
        VBox.addWidget(self.bt_bid)
        self.setLayout(VBox)
        self.show()

    #点击出价按钮
    def bt_bid_clicked(self):
        #检查输入
        regex_money = '^\d+$'
        #清除原有输入
        money = self.bid_input.text()
        self.bid_input.setText("")
        rr1 = re.compile(regex_money)
        if rr1.match(money) is None:
            QMessageBox.warning(self, "warning!", "invalid input")
            return 1
        #在数据表bidding中加入出价
        bid_id = str(money)+"00"  #这个乱来的
        sql = 'insert into bidding(bid_id, datapkg_id, buyer_id, price) values(%s,%s,%s,%s);' #虽然表里是float，但是这里还是%s
        value_list = [bid_id, self.bid_datapkg_id, self.buyer_id, money]
        print("sql=", sql)
        print("value_list=", value_list)
        db = connect2db()
        cursor = db.cursor()
        cursor.execute(sql, value_list)
        db.commit()
        print("db.commit success")
        cursor.close()
        db.close()
        row_list = ["bid_id", "datapkg_id", "buyer_id", "price"]
        #db_add_one_row("bidding", row_list, value_list)
        QMessageBox.warning(self, "notion", "successfully bid. The result will be sent be your email address after the bid finish")
