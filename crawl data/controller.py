import requests
from config import *

class Controller:
  @staticmethod
  def create_payload(method = None, params = None):
    payload = {
      "apikey": API_KEY,
      "method": method,
    }

    for key, value in params.items():
      param = f"param[{key}]"
      payload[param] = value

    return payload

  @staticmethod
  def get_list_model(model_name=None):
    params = {
      "model_name": model_name if model_name else '',
    }
    payload = Controller.create_payload(method = "list_models", params = params)


    r = requests.post(API_URL, data=payload)

    data = r.json()

    print("daily_hits_left: {}".format(data["daily_hits_left"]))

    return data["result"]

  @staticmethod
  def get_model_info(model_id):
    params = {
      "model_id": model_id
    }
    payload = Controller.create_payload(method="get_model_info", params = params)

    r = requests.post(API_URL, data=payload)

    data = r.json()

    print("daily_hits_left: {}".format(data["daily_hits_left"]))

    return data["result"]["0"] if data["result"] else None

  @staticmethod
  def get_model_info_all(model_id):
    params = {
      "model_id": model_id
    }
    payload = Controller.create_payload(method="get_model_info_all", params = params)

    r = requests.post(API_URL, data=payload)

    data = r.json()

    print("daily_hits_left: {}".format(data["daily_hits_left"]))

    return data["result"]["0"] if data["result"] else None

  @staticmethod
  def get_conf_info(config):
    payload = Controller.create_payload(method="get_conf_info", params=config)

    r = requests.post(API_URL, data=payload)

    data = r.json()

    print("daily_hits_left: {}".format(data["daily_hits_left"]))

    return data["result"] if data["result"] else None
