HOST = 'rm-uf64u9qj410or7qhgto.mysql.rds.aliyuncs.com'
USER = 'user'
PASSWORD = 'Qwer123!'
DATABASE = 'database_test'

class DatabaseConfig:
  host: str
  user: str
  password: str
  database: str

  def __init__(self):
    self.host = HOST
    self.user = USER
    self.password = PASSWORD
    self.database = DATABASE
