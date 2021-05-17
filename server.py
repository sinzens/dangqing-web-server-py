from typing import Any, Dict
from websocket_server import WebsocketServer
from database import Database
from database_config import DatabaseConfig
from json_converter import JsonConverter

class Server:
  server: WebsocketServer
  database: Database
  commands: Dict[str, Any]

  def __init__(self, host: str, port: int):
    self.server = WebsocketServer(host=host, port=port)
    self.server.set_fn_new_client(self.new_client)
    self.server.set_fn_message_received(self.message_received)
    self.database = Database(DatabaseConfig())
    self.converter = JsonConverter()

    self.commands = {
      'getVersion': self.on_get_version,
      'getBatches': self.on_get_batches,
      'getPathsAtd': self.on_get_paths_atd,
      'getPathsDta': self.on_get_paths_dta,
      'deleteItem': self.on_delete_item,
      'insertItem': self.on_insert_item,
      'updateItem': self.on_update_item,
      'exit': self.on_exit
    }

  def run(self):
    self.server.run_forever()

  def new_client(self, client, server):
    print('New connection from: %s.' % client['id'])

  def client_left(self, client, server):
    print('Connection from %s closed.' % client['id'])

  def message_received(self, client, server: WebsocketServer, message: str):
    # print('Received from client: %s, message: %s' % (client['id'], message))
    message = message.encode('raw_unicode_escape').decode('utf-8')
    if not message.startswith('cmd'):
      return
    messages = message.split('|')
    command = messages[1]
    handler = self.commands.get(command)

    if not handler is None:
      if (
        command == 'deleteItem' or
        command == 'insertItem'
      ):
        handler(client, server, messages[2], messages[3])
      elif command == 'updateItem':
        handler(client, server, messages[2], messages[3], messages[4])
      else:
        handler(client, server)

  def on_get_version(self, client, server: WebsocketServer):
    version = self.database.get_version()
    server.send_message(client, 'res|version|%s' % version[0])

  def on_get_batches(self, client, server: WebsocketServer):
    batches = self.database.get_batches()
    json_data = self.converter.batches_to_json(batches)
    server.send_message(client, 'res|batches|%s' % json_data)

  def on_get_paths_atd(self, client, server: WebsocketServer):
    paths = self.database.get_paths_atd()
    json_data = self.converter.paths_atd_to_json(paths)
    server.send_message(client, 'res|pathsAtd|%s' % json_data)

  def on_get_paths_dta(self, client, server: WebsocketServer):
    paths = self.database.get_paths_dta()
    json_data = self.converter.paths_dta_to_json(paths)
    server.send_message(client, 'res|pathsDta|%s' % json_data)

  def on_delete_item(
    self, client, server: WebsocketServer, table: str,
    json_data: str,
  ):
    if table == 'batch':
      json_data = self.converter.batch_json_to_tuple(json_data)
      self.database.delete_item_batch(json_data)
    if table == 'atdPath':
      json_data = self.converter.path_atd_json_to_tuple(json_data)
      self.database.delete_item_path_atd(json_data)
    if table == 'dtaPath':
      json_data = self.converter.path_dta_json_to_tuple(json_data)
      self.database.delete_item_path_dta(json_data)

  def on_insert_item(
    self, client, server: WebsocketServer, table: str,
    json_data: str,
  ):
    if table == 'batch':
      json_data = self.converter.batch_json_to_tuple(json_data)
      self.database.insert_item_batch(json_data)
    if table == 'atdPath':
      json_data = self.converter.path_atd_json_to_tuple(json_data)
      self.database.insert_item_path_atd(json_data)
    if table == 'dtaPath':
      json_data = self.converter.path_dta_json_to_tuple(json_data)
      self.database.insert_item_path_dta(json_data)

  def on_update_item(
    self, client, server: WebsocketServer, table: str,
    json_data: str,
    json_data_before: str
  ):
    if table == 'batch':
      json_data = self.converter.batch_json_to_tuple(json_data)
      json_data_before = self.converter.batch_json_to_tuple(json_data_before)
      self.database.update_item_batch(json_data, json_data_before)
    if table == 'atdPath':
      json_data = self.converter.path_atd_json_to_tuple(json_data)
      json_data_before = self.converter.path_atd_json_to_tuple(json_data_before)
      self.database.update_item_path_atd(json_data, json_data_before)
    if table == 'dtaPath':
      json_data = self.converter.path_dta_json_to_tuple(json_data)
      json_data_before = self.converter.path_dta_json_to_tuple(json_data_before)
      self.database.update_item_path_dta(json_data, json_data_before)

  def on_exit(self, client, server: WebsocketServer):
    server.server_close()
