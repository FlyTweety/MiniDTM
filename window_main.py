#coding = 'utf-8'

from database_funs import * #数据库有关操作函数
from hash_funs import * #哈希有关函数
from window_buyer import * #买家界面
from window_seller import * #卖家界面
from window_middleman import * #中间商界面

import sys
from PyQt5.QtWidgets import (QInputDialog, QLabel, QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, QMessageBox, QTableWidget, QAction, QTableWidgetItem)
from PyQt5.QtGui import QFont, QPalette, QPixmap, QBrush, QIcon
from PyQt5.QtCore import Qt
from PyQt5.Qt import *
import re

#文件路径大合集
ICON_PATH = './images/bg_son.jpg'
WELCOME_BG_PATH = "./images/bg_son.jpg"

##欢迎界面##################################################################################################################################
class Window_Welcome(QWidget):
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
        #设置该窗口元素
        self.Init_UI()

    def Init_UI(self):
        #窗口设置
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT) 
        self.setWindowTitle('MiniDTM')
        self.setWindowIcon(QIcon(ICON_PATH))
        #背景图片
        palette = QPalette()
        pix=QPixmap(WELCOME_BG_PATH)
        pix = pix.scaled(self.width(),self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        #顶部标题
        top_label = QLabel(self)
        top_label.setText("MiniDTM: A Mini Data Trade Market")
        top_label.setStyleSheet("color: cornsilk")
        top_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        top_label.setFont(font)
        #底部四个按钮
        bt_login  = QPushButton('Login/Register', self)
        bt_info   = QPushButton('About Us', self)
        bt_thanks = QPushButton('Thanks', self)
        bt_history = QPushButton('History Hash', self)
        bt_login.clicked.connect(self.login_bt_clicked)
        bt_info.clicked.connect(self.info_bt_clicked)
        bt_thanks.clicked.connect(self.thanks_bt_clicked)
        bt_history.clicked.connect(self.gen_history_hash)
        #显示布局设置
        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(top_label)
        vbox.addStretch(7)
        vbox.addWidget(bt_login)
        vbox.addWidget(bt_info)
        vbox.addWidget(bt_thanks)
        vbox.addWidget(bt_history)
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.show()

    # login按钮点击
    def login_bt_clicked(self):
        window_login = Window_Login()
        window_login.exec()

    # info按钮点击
    def info_bt_clicked(self):
        QMessageBox.about(self, 'info','MiniDTM: a mini data trade market softerware written by ChenyangZhu')

    # thanks按钮点击
    def thanks_bt_clicked(self):
        QMessageBox.about(self, 'thanks','Thanks List: \nthe builder of PyQt\npymysql\npyap\nLAC\nnumpy\npandas\nsklearn\nlibsvm\nhashlib')

    # 生成历史区块按钮
    def gen_history_hash(self):
        all_history = db_get_table_datas('history')
        #获取所有历史的哈希块
        history_blocks = []
        for i in range(len(all_history)):
            if(all_history[i]['hash']!=None):
                history_blocks.append(all_history[i]['hash'])
        #如果最近一次交易记录没有生成新的哈希块，则生成
        if(all_history[len(all_history)-1]['hash']==None):
            history_str = ''
            if(len(history_blocks)>1): #加上最近一块的哈希值
                history_str += history_blocks[len(history_blocks)-1]
            history_str += all_history[len(all_history)-1]['name']
            history_str += all_history[len(all_history)-1]['buyer']
            history_str += all_history[len(all_history)-1]['middleman']
            new_hash = genearteMD5(history_str)
            history_blocks.append(new_hash)
            #将最近的结果写入数据库
            this_id =  all_history[len(all_history)-1]['id']
            print("new_hash=", new_hash)
            print("id=", this_id)
            db = connect2db()
            cursor = db.cursor()
            sql = 'update history set hash = \'' + str(new_hash) + '\' where id = ' + str(this_id)
            print(sql)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
        #弹窗显示结果
        showcase_str = 'History Blocks are : \n'
        for i in range(len(history_blocks)):
            showcase_str += str(i)
            showcase_str += ': '
            showcase_str += history_blocks[i]
            showcase_str += '\n'
        QMessageBox.information(self, 'info', showcase_str)

##登录界面##################################################################################################################################
class Window_Login(QDialog):
    def __init__(self):
        super().__init__()
        #获取屏幕分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        #设置窗口大小
        self.HEIGHT = int(self.screenRect.height() * 0.2)
        self.WIDTH = int(self.screenRect.width() * 0.3)
        self.TOP = int(self.screenRect.height() * 0.4)
        self.LEFT = int(self.screenRect.width() * 0.35)
        #初始化
        self.Init_UI()

    def Init_UI(self):
        #窗口设置
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT) 
        self.setWindowTitle('MiniDTM_Login')
        self.setWindowIcon(QIcon(ICON_PATH))
        #账号输入框
        self.edit_account  = QLineEdit(self)
        self.edit_account.setPlaceholderText("account, 6 number")
        self.edit_account.setClearButtonEnabled(True)
        #密码输入框
        self.edit_password = QLineEdit(self)
        self.edit_password.setPlaceholderText("password, 6 number or character")   
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setClearButtonEnabled(True)
        #六个按钮
        self.bt_buy_login = QPushButton('买家登录', self)
        self.bt_mid_login = QPushButton('中间商登录', self)
        self.bt_sell_login = QPushButton('卖家登录', self)
        self.bt_buy_register = QPushButton('买家注册', self)
        self.bt_mid_register = QPushButton('中间商注册', self)
        self.bt_sell_register = QPushButton('卖家注册', self)
        self.bt_buy_login.clicked.connect(self.bt_login_clicked)
        self.bt_mid_login.clicked.connect(self.bt_login_clicked)
        self.bt_sell_login.clicked.connect(self.bt_login_clicked)
        self.bt_buy_register.clicked.connect(self.bt_register_clicked)
        self.bt_mid_register.clicked.connect(self.bt_register_clicked)
        self.bt_sell_register.clicked.connect(self.bt_register_clicked)
        #显示布局设置
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.edit_account)
        vbox.addWidget(self.edit_password)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.bt_buy_login)
        hbox1.addWidget(self.bt_mid_login)
        hbox1.addWidget(self.bt_sell_login)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.bt_buy_register)
        hbox2.addWidget(self.bt_mid_register)
        hbox2.addWidget(self.bt_sell_register)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)
        self.show()
    
    # 点击登录按钮
    def bt_login_clicked(self):
        account_str = self.edit_account.text()
        password_str = self.edit_password.text()
        self.edit_account.setText("")
        self.edit_password.setText("")
        sender = self.sender()
        if(not ((len(account_str)==6) and (len(password_str)==6))):
            QMessageBox.warning(self, 'warning!','invalid input')
            return 1
        if(sender == self.bt_buy_login):
            if(self.db_query_user(account_str, password_str, table="buyer") == True):
                window_buyer_main = Window_Buyer_Main()
                window_buyer_main.buyer_id = account_str  #传递登录时买家的ID
                window_buyer_main.exec()
            else:
                QMessageBox.warning(self, 'warning!','buyer not found')
        elif(sender == self.bt_mid_login):
            if(self.db_query_user(account_str, password_str, table="middleman") == True):
                window_middleman_main = Window_Middleman_Main()
                window_middleman_main.middleman_id = account_str  #传递登录时中间商的ID
                window_middleman_main.exec()
            else:
                QMessageBox.warning(self, 'warning!','middleman not found')
        elif(sender == self.bt_sell_login):
            if(self.db_query_user(account_str, password_str, table="seller") == True):
                window_seller_main = Window_Seller_Main()
                window_seller_main.seller_id = account_str  #传递登录时卖家的ID
                window_seller_main.exec()
            else:
                QMessageBox.warning(self, 'warning!','seller not found')
    
    # 点击注册按钮
    def bt_register_clicked(self):
        #检查输入是否符合格式
        account_str = self.edit_account.text()
        password_str = self.edit_password.text()
        self.edit_account.setText("")
        self.edit_password.setText("")
        if(not ((len(account_str)==6) and (len(password_str)==6))):
            QMessageBox.warning(self, 'warning!','invalid input')
            return 1
        sender = self.sender()
        if(sender == self.bt_buy_register):
            self.db_add_user(account_str, password_str, table = 'buyer')
            QMessageBox.warning(self, 'notion!','successfully register buyer!')
        elif(sender == self.bt_mid_register):
            self.db_add_user(account_str, password_str, table = 'middleman')
            QMessageBox.warning(self, 'notion!','successfully register middleman!')
        elif(sender == self.bt_sell_register):
            self.db_add_user(account_str, password_str, table = 'seller')
            QMessageBox.warning(self, 'notion!','successfully register seller!')

    # 登录时检查用户
    def db_query_user(self, account_str, password_str, table = None):
        db = connect2db()
        cursor = db.cursor()
        sql = 'select * from %s where account = "%s" and password="%s"' % (table, account_str, password_str)
        res = cursor.execute(sql)
        cursor.close()
        db.close()
        if res:
            return True
        else:
            return False

    # 注册新用户
    def db_add_user(self, account_str, password_str, table = None):
        db = connect2db()
        cursor = db.cursor()
        sql = 'insert into ' + str(table) + '(account, password) values(%s,%s);'
        cursor.execute(sql, [account_str, password_str])
        db.commit()
        cursor.close()
        db.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_welcome = Window_Welcome()
    app.exit(app.exec_())