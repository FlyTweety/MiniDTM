import pandas as pd
import numpy as np
from database_funs import *

size = [] 
accuracy = []    
price = []

#通过随机数生成历史
for i in range(1,51):
    size.append(i+np.random.random()*i)
    accuracy.append(i+2*np.random.random()*i)
    price.append(i+np.random.random()*i)

#字典中的key值即为csv中列名
dataframe = pd.DataFrame({'size': size, 'accuracy': accuracy, 'price': price})

#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe.to_csv("./datas/history_price.csv",index=False,sep=',')

#保存到mysql
