这是MiniDTM
主函数是window_main.py，运行此函数即可得到窗口。由于调库较多，启动时可能会花费1-5秒时间
想要运行此项目，请确保：
1. 安装了python3
2. 安装了MySQL
3. 安装了requirements文件夹下requirements.txt所列出的所有python依赖组件
4. 将sql文件夹下的minidtm.sql文件导入到mysql，构建minidtm数据库
5. 修改database_funs.py中对本地mysql的连接账号密码，确保能够实现本地连接并打开minidtm数据库
6. 电脑有着不太过于小的内存空间与不至于慢得离谱的CPU
7. 其他要求详见MiniDTM项目报告书
其他：部分功能如联邦学习、计算shapley值部分计算量较大，运行速度较慢，可能需要30秒以上的等待，程序可能提示无响应，耐心等待即可