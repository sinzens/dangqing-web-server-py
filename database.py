import pymysql
from database_config import DatabaseConfig

class Database:
  connection: pymysql.connections.Connection
  config: DatabaseConfig

  def __init__(self, config: DatabaseConfig):
    self.config = config
    self.connect()

  def __del__(self):
    self.disconnect()

  def connect(self):
    self.connection = pymysql.connect(
      host = self.config.host,
      user = self.config.user,
      password = self.config.password,
      database = self.config.database
    )

  def disconnect(self):
    self.connection.close()

  def commit(self):
    self.connection.commit()

  def roll_back(self):
    self.connection.rollback()

  def get_single_data(self, sql: str):
    cursor = self.connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    return data

  def get_multi_data(self, sql: str):
    cursor = self.connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data

  def set_data(self, sql: str):
    cursor = self.connection.cursor()
    try:
      cursor.execute(sql)
      self.commit()
    except:
      self.roll_back()
    cursor.close()

  def get_version(self):
    return self.get_single_data('select version()')

  def get_batches(self):
    return self.get_multi_data('select * from batch;')

  def get_paths_atd(self):
    return self.get_multi_data('select * from path_1;')

  def get_paths_dta(self):
    return self.get_multi_data('select * from path_2;')

  def delete_item_batch(self, json_data: str):
    self.set_data(
      'delete from batch where batchno=%s;' %
      json_data[0]
    )

  def delete_item_path_atd(self, json_data: str):
    self.set_data(
      'delete from path_1 where area=\'%s\' and destination=\'%s\';' %
      (json_data[0], json_data[2])
    )

  def delete_item_path_dta(self, json_data: str):
    self.set_data(
      'delete from path_2 where name=\'%s\';' %
      json_data[0]
    )

  def insert_item_batch(self, json_data: str):
    self.set_data(
      'insert into batch values(%s, %s, %s, \'%s\', %s, \'%s\', %s);' %
      json_data
    )

  def insert_item_path_atd(self, json_data: str):
    self.set_data(
      'insert into path_1 values(\'%s\', \'%s\', \'%s\', \'%s\');' %
      json_data
    )

  def insert_item_path_dta(self, json_data: str):
    self.set_data(
      'insert into path_2 values(\'%s\', \'%s\', \'%s\', %s, \'%s\');' %
      json_data
    )

  def update_item_batch(self, json_data: str, json_data_before: str):
    self.set_data(
      '''
      update batch set
        batchno=%s,
        arrialtime=%s,
        arrivalnum=%s,
        dropoff_no=\'%s\',
        stand_no=%s,
        security_no=\'%s\',
        sc_capacity=%s
      where batchno=%s;
      ''' % (json_data + (json_data_before[0],))
    )

  def update_item_path_atd(self, json_data: str, json_data_before: str):
    self.set_data(
      '''
      update path_1 set
        area=\'%s\',
        name=\'%s\',
        destination=\'%s\',
        path=\'%s\'
      where area=\'%s\' and destination=\'%s\';
      ''' % (json_data + (json_data_before[0], json_data_before[2]))
    )

  def update_item_path_dta(self, json_data: str, json_data_before: str):
    self.set_data(
      '''
      update path_2 set
        name=\'%s\',
        content=\'%s\',
        security_no=\'%s\',
        areanumber=%s,
        path=\'%s\'
      where name=\'%s\';
      ''' % (json_data + (json_data_before[0],))
    )
