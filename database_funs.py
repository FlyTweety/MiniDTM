##数据库查询##################################################################################################################################
import pymysql

#连接数据库
def connect2db():
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='Lszcy1125',
                     database='minidtm',
                     charset='utf8')
    return db

# 获取表头
def db_get_col_list(table_name):
    db = connect2db()
    cursor = db.cursor()
    cursor.execute("select * from %s" % table_name)
    col_name_list = [tuple[0] for tuple in cursor.description]
    cursor.close()
    db.close()
    return col_name_list

# 获取表中数据，字典形式返回
def db_get_table_datas(table_name):
    db = connect2db()
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from %s;' % table_name
    cursor.execute(sql)
    ret = cursor.fetchall()
    cursor.close()
    db.close()
    return ret

# 附带条件，获取表中数据，字典形式返回
def db_get_table_datas_with_constraint(table_name, constraint):
    db = connect2db()
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from %s where ' % table_name
    sql += constraint
    sql += ';'
    print("sql=", sql)
    cursor.execute(sql)
    ret = cursor.fetchall()
    cursor.close()
    db.close()
    return ret

# 在数据表中新增行
def db_add_one_row(table_name, row_list, value_list):
    db = connect2db()
    cursor = db.cursor()
    #智能构建sql执行字符串
    sql = 'insert into ' + table_name + '('
    for i in range(len(row_list)):
        sql += row_list[i]
        if(i == len(row_list)-1):
            sql += ')'
        else:
            sql += ', '
    sql += " values("
    for i in range(len(value_list)):
        sql += '\''
        sql += value_list[i]
        if(i == len(value_list)-1):
            sql += '\');'
        else:
            sql += '\', '
    print("sql=", sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

#创建表
def db_create_table(name, rows, kinds): 
    db = connect2db()
    cursor = db.cursor()
    print("rows=",rows,"\nkinds=",kinds)
    sql = 'create table ' + name + '('
    for i in range(len(rows)):
        #目前还有问题是建表需要主键，决定自己加序号当主键
        if(i == 0):
            sql += 'row_index int(4) primary key not null auto_increment, '
        #名字不能单纯数字，而目前生成的方法就是数字，所以手动加上字母'row_'
        sql += 'row_'
        sql += rows[i]
        sql += ' '
        sql += kinds[i]
        if(i == len(rows)-1):
            sql += ');'
        else:
            sql += ', '
    print("sql=", sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

# 在数据表中新增行with每行前缀
def db_add_one_row_with_prefix(table_name, row_list, value_list, row_prefix=None):
    db = connect2db()
    cursor = db.cursor()
    #智能构建sql执行字符串
    sql = 'insert into ' + table_name + '('
    for i in range(len(row_list)):
        #构建前缀
        if(row_prefix!=None):
            sql += row_prefix
        sql += row_list[i]
        if(i == len(row_list)-1):
            sql += ')'
        else:
            sql += ', '
    sql += " values("
    for i in range(len(value_list)):
        sql += '\''
        sql += value_list[i]
        if(i == len(value_list)-1):
            sql += '\');'
        else:
            sql += '\', '
    print("sql=", sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()