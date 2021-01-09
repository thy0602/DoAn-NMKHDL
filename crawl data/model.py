from feature import *

class Laptop:
    def __init__(self, data):
        self.features = {
            "producer": Producer(data["model_info"][0]),
            "processor": Processor(data["cpu"]),
            "ram": Ram(data["memory"]),
            "hdd_storage": HDDStorage(data),
            "ssd_storage":SSDStorage(data),
            "graphic": Graphic(data["gpu"]),
            "screen": Screen(data["display"]),
            "weight": Chassis(data["chassis"]),
            "os": OperatingSystem(data["operating_system"])
        }
        self.price = (int(data["config_price_min"]) + int(data["config_price_max"])) / 2

    def is_valid(self):
        for key, feature in self.features.items():
            if not feature.is_valid():
                return False
        return True

    def __str__(self):
        feature_list = list(self.features)
        return ','.join(map(str, (self.features[key] for key in feature_list))).strip() + ',' + str(self.price)

if __name__ == '__main__':
    print("Model test")
    laptop = Laptop({"model_info": {
        "id": 1175,
        "noteb_name":"Dell Inspiron",
        "name": "Dell Inspiron"
    }, "cpu": {
        "prod": "Intel",
        "model": "i5-7Y54"
    }, "config_id": "123123"})

    print(laptop.processor.model)
