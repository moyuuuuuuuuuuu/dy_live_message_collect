class Config(object):
    config = {}
    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            Config._instance = Config(*args, **kwargs)
        return Config._instance

    def setConfig(self, **config):
        self.config = config

    def get(self, key):
        return self.config.get(key)
