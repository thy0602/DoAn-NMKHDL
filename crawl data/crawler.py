import os
import json
import random
from copy import deepcopy

from config import *
from feature_domain import *
from model import Laptop
from controller import Controller

class Crawler:
  def __init__(self):
    self.models = None
    self.cached_model = self.get_cache(file_name=MODEL_CACHE_FILE)
    self.cached_configurate_id = self.get_cache(file_name=CONFIGURATE_ID_CACHE_FILE)
    self.cached_gen_configurate = self.get_cache(file_name=GEN_CONFIGURATE_CACHE_FILE)

  def get_cache(self, file_name):
    if not os.path.isfile(file_name):
      return set()

    cached = set()
    with open(file_name) as f:
      for line in f:
        cached.add(int(line))

    return cached

  def get_conf_hash(self, configure):
    hashed = hash(frozenset(configure.items()))
    return hashed

  def generate_configurate(self, model_info_all):
    configures = []
    tried = 0
    MAX_ATTEMPT  = 20
    success_generated = 0
    MAX_GENERATE = 2

    while tried < MAX_ATTEMPT and success_generated < MAX_GENERATE:
      tried  += 1
      configure = {}
      info = {}
      changed = False

      for feature, config in feature_config_map.items():
        if feature == "model_info":
          configure["model_id"] = model_info_all["model_info"][0]["id"]
          info["model_info"] = model_info_all["model_info"]
          continue

        configure[config["param"]] = str(model_info_all[feature]["selected"])

        if "allow_custom" in config:
          options = list(model_info_all[feature].keys())

          options.remove(str(model_info_all[feature]["selected"]))
          options.remove("selected")

          if len(options) > 0:
            configure[config["param"]] = random.choice(options)
            changed = True

        info[feature] = model_info_all[feature][configure[config["param"]]]

      config_hash = self.get_conf_hash(configure)
      if changed and config_hash not in self.cached_gen_configurate:
        success_generated += 1
        self.cached_gen_configurate.add(config_hash)
        configures.append((configure, info))

    return configures

  def save_model(self, data):
    headers = "producer, processor prod, processor model, cores, core base speed (GHz), ram type, ram cap (GB), ssd (GB), hdd (GB), gpu prod, gpu size (MB), screen type, screen size (inch), weight (kg), os, price(USD)\n"

    with open("data.csv", "a") as f:
      if os.path.getsize("data.csv") == 0:
        f.write(headers)
      f.write(f"{data}\n")

  def save_gen_configurate(self, configurate_id):
    with open(GEN_CONFIGURATE_CACHE_FILE, "a") as f:
      f.write(f"{configurate_id}\n")

  def save_cache(self):
    with open(CONFIGURATE_ID_CACHE_FILE, "w") as f:
      for config_id in self.cached_configurate_id:
        f.write(f"{config_id}\n")

    with open(MODEL_CACHE_FILE, "w") as f:
      for model_id in self.cached_model:
        f.write(f"{model_id}\n")

  def crawl_with_custom_config(self, producers=[None]):
    for producer in producers:
      models = Controller.get_list_model(model_name=producer)
      for model in models.values():
        model_id = model["model_info"][0]["id"]

        print(f"Generate configuration for model {model_id}")

        model_info_all = Controller.get_model_info_all(model_id)


        if not model_info_all:
          print("Empty info {}".format(model_id))
          continue

        gen_configures = self.generate_configurate(model_info_all)

        print(f"Generated {len(gen_configures)} config")

        saved_model = 0

        for config, model_info in gen_configures:
          extra_info = Controller.get_conf_info(config)

          if not extra_info:
            continue

          model_info["config_price_min"] = extra_info["config_price_min"]
          model_info["config_price_max"] = extra_info["config_price_max"]

          laptop = Laptop(model_info)

          if laptop.is_valid():
            self.save_model(laptop)
            self.save_gen_configurate(self.get_conf_hash(config))
            print(laptop)
            saved_model += 1

        print(f"Successful save {saved_model} generate model\n")

  def crawl(self, producers=[None]):
    for producer in producers:
      models = Controller.get_list_model(model_name=producer)

      for model in models.values():
        model_id = model["model_info"][0]["id"]
        if model_id in self.cached_model:
          print(f"Ignore model {model_id}")
          continue
        print(f"Crawl model {model_id}")

        model_info = Controller.get_model_info(model_id)

        if model_info is None:
          print("Empty info :(")
          continue

        laptop = Laptop(model_info)

        if laptop.is_valid():
          config_id = int(model_info["config_id"])
          if config_id in self.cached_configurate_id:
            print("Configuration already save")
            continue
          self.cached_configurate_id.add(config_id)
          self.cached_model.add(model_id)
          self.save_model(laptop)
          self.save_cache()
          print(f"{laptop}\n")
