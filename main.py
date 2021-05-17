# import socket
# import threading
# import pymysql

# # host = 'rm-uf64u9qj410or7qhgto.mysql.rds.aliyuncs.com'
# # user = 'user'
# # password = 'Qwer123!'
# # database = 'work_db'
# # port = 3306
# # connectTimeout = 5000

# connection = pymysql.connect(host = host, user = user, password = password, database = database, charset = 'utf8')

from server import Server

if __name__ == '__main__':
  server = Server('localhost', 11037)
  server.run()
