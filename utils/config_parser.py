class ConfigParser(object):
    def __init__(self, settings):
        self.settings = settings

    def parse(self, files):
        env = {}
        for file in files:
            exec file.read() in env
        env.pop("__builtins__")
        self.settings.update(env)


def config_parser(files, settings={}):
    cp = ConfigParser(settings)
    cp.parse(files)
