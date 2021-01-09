producer_domain = {"apple", "asus", "hp", "lenovo", "lg", "dell", "acer"}
processor_name_domain = {"intel", "amd", "cpu"}
processor_model_domain = {"i3", "i5", "i7", "ryzen 5", "ryzen 3", "ryzen 7", "integrated"}

config_map = {
  "model_info": "mode_id",
  "cpu": "cpu_id",
  "display": "display_id",
  "memory": "memory_id",
  "primary_storage": "primary_storage_id",
  "secondary_storage": "secondary_storage_id",
  "gpu": "gpu_id",
  "wireless": "wireless_id",
  "optical_drive": "optical_drive_id",
  "motherboard": "motherboard_id",
  "chassis": "chassis_id",
  "battery": "battery_id",
  "warranty": "warranty_id",
  "operating_system": "operating_system_id"
}

feature_config_map = dict()

for key, value in config_map.items():
  feature_config_map[key] = {
    "param": value
  }

require_feature = ["memory", "primary_storage", "secondary_storage", "operating_system"]
for feature in require_feature:
  feature_config_map[feature]["allow_custom"] = True
