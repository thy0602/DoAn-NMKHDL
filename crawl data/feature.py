from feature_domain import *

class Feature:
    def __init__(self):
        pass

    def is_valid(self):
        pass

class Producer(Feature):
    def __init__(self, data):
        self.name = self.extract_name(data["noteb_name"])

    def extract_name(self, raw_name):
        raw_name = raw_name.strip().lower()
        for producer_name in producer_domain:
            if raw_name.find(producer_name) != -1:
                return producer_name

        return "N/A"

    def is_valid(self):
        return self.name in producer_domain

    def __str__(self):
        return self.name

class Processor(Feature):
    def __init__(self, data):
        self.name = data["prod"].strip().lower()
        self.model = self.extract_model(data["model"])
        self.cores = int(data["cores"])
        self.core_speed = float(data["base_speed"])

    def extract_model(self, raw_model):
        raw_model = raw_model.strip().lower()
        for model_name in processor_model_domain:
            if raw_model.find(model_name) != -1:
                return model_name
        return "N/A"

    def is_valid(self):
        return self.name in processor_name_domain and self.model in processor_model_domain

    def __str__(self):
        return f"{self.name}, {self.model}, {self.cores}, {self.core_speed}"

class Ram(Feature):
    def __init__(self, data):
        self.type = data["type"].strip().lower()
        self.size = int(data["size"])

    def is_valid(self):
        return isinstance(self.size, int) and self.size > 0

    def __str__(self):
        return self.type + ', ' + str(self.size)

class HDDStorage(Feature):
    def __init__(self, data):
        self.size = self.extract_size(data)

    def extract_size(self, data):
        total = 0
        keys = ["primary_storage", "secondary_storage"]
        for key in keys:
            if data[key]["model"].find("HDD") != -1:
                total += int(data[key]["cap"])
        return total

    def is_valid(self):
        return isinstance(self.size, int) and self.size >= 0

    def __str__(self):
        return str(self.size)

class SSDStorage(Feature):
    def __init__(self, data):
        self.size = self.extract_size(data)

    def extract_size(self, data):
        total = 0
        keys = ["primary_storage", "secondary_storage"]
        for key in keys:
            if data[key]["model"].find("SSD") != -1:
                total += int(data[key]["cap"])
        return total

    def is_valid(self):
        return isinstance(self.size, int) and self.size >= 0

    def __str__(self):
        return str(self.size)

class Graphic(Feature):
    def __init__(self, data):
        self.size = int(data["memory_size"])
        self.prod = data["prod"].strip().lower()

    def is_valid(self):
        return isinstance(self.size, int) and isinstance(self.prod, str) and self.size > 0

    def __str__(self):
        return f"{self.prod}, {self.size}"

class Screen(Feature):
    def __init__(self, data):
        self.size = float(data["size"])
        self.type = data["type"].strip().lower()

    def is_valid(self):
        return isinstance(self.size, float) and isinstance(self.type, str) and self.size > 0

    def __str__(self):
        return f"{self.type}, {self.size}"

class Chassis(Feature):
    def __init__(self, data):
        self.weight = float(data["weight_kg"])

    def is_valid(self):
        return isinstance(self.weight, float) and self.weight > 0

    def __str__(self):
        return str(self.weight)

class OperatingSystem(Feature):
    def __init__(self, data):
        if isinstance(data, str):
            self.name = data.strip().lower()
        else:
            self.name = data["name"].strip().lower()

    def is_valid(self):
        return isinstance(self.name, str)

    def __str__(self):
        return self.name
