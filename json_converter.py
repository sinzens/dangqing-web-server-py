import json
import tablib

class JsonConverter:
  def __init__(self):
    pass

  def batch_to_dict(self, batch):
    batch_str = ['%s' % value for value in batch]
    return {
      'batchNo': batch_str[0],
      'arrivalTime': batch_str[1],
      'arrivalNum': batch_str[2],
      'dropOffNo': batch_str[3],
      'standNo': batch_str[4],
      'securityNo': batch_str[5],
      'scCapacity': batch_str[6]
    }

  def path_atd_to_dict(self, path):
    path_str = ['%s' % value for value in path]
    return {
      'area': path_str[0],
      'name': path_str[1],
      'destination': path_str[2],
      'path': path_str[3]
    }

  def path_dta_to_dict(self, path):
    path_str = ['%s' % value for value in path]
    return {
      'name': path_str[0],
      'content': path_str[1],
      'securityNo': path_str[2],
      'areaNumber': path_str[3],
      'path': path_str[4]
    }

  def batches_to_json(self, batches):
    batches_list = []
    for batch in batches:
      dict = self.batch_to_dict(batch)
      batches_list.append(dict)
    return json.dumps(batches_list)

  def paths_atd_to_json(self, paths):
    paths_list = []
    for path in paths:
      dict = self.path_atd_to_dict(path)
      paths_list.append(dict)
    return json.dumps(paths_list)

  def paths_dta_to_json(self, paths):
    paths_list = []
    for path in paths:
      dict = self.path_dta_to_dict(path)
      paths_list.append(dict)
    return json.dumps(paths_list)

  def batch_json_to_tuple(self, json_data: str):
    data = json.loads(json_data)
    return (
      data['batchNo'],
      data['arrivalTime'],
      data['arrivalNum'],
      data['dropOffNo'],
      data['standNo'],
      data['securityNo'],
      data['scCapacity']
    )

  def path_atd_json_to_tuple(self, json_data: str):
    data = json.loads(json_data)
    return (
      data['area'],
      data['name'],
      data['destination'],
      data['path']
    )

  def path_dta_json_to_tuple(self, json_data: str):
    data = json.loads(json_data)
    return (
      data['name'],
      data['content'],
      data['securityNo'],
      data['areaNumber'],
      data['path']
    )

  def batches_json_to_tuple(self, json_data: str):
    data_array = json.loads(json_data)
    return list(map(
      lambda data: (
        data['batchNo'],
        data['arrivalTime'],
        data['arrivalNum'],
        data['dropOffNo'],
        data['standNo'],
        data['securityNo'],
        data['scCapacity']
      ),
      data_array
    ))

  def paths_atd_json_to_tuple(self, json_data: str):
    data_array = json.loads(json_data)
    return list(map(
      lambda data: (
        data['area'],
        data['name'],
        data['destination'],
        data['path']
      ),
      data_array
    ))

  def paths_dta_json_to_tuple(self, json_data: str):
    data_array = json.loads(json_data)
    return list(map(
      lambda data: (
        data['name'],
        data['content'],
        data['securityNo'],
        data['areaNumber'],
        data['path']
      ),
      data_array
    ))

  def json_to_excel(self, json_data: str):
    data = json.loads(json_data)
    headers = tuple([attr for attr in data[0].keys()])

    excel_data = []
    for obj in data:
      body = [value for value in obj.values()]
      excel_data.append(tuple(body))

    excel_data = tablib.Dataset(*excel_data, headers=headers)
    return excel_data
