import yaml

class ConfigManager:
    _instance = None
    _config = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def initialize(cls, config_path="./util/resources/config.yaml"):
        if cls._config is None:
            try:
                with open(config_path, "r") as file:
                    cls._config = yaml.safe_load(file)
            except FileNotFoundError:
                cls._config = {}
            except yaml.YAMLError as e:
                raise ValueError(f"Erro ao processar o arquivo YAML: {e}")

    @classmethod
    def get(cls, key, default=None):
        if cls._config is None:
            raise ValueError("Erro ao processsar get. Inicialize com initialize()")

        keys = key.split('.')
        value = cls._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value