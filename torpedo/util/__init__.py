__author__ = 'kbroughton'

class PluginLoader(object):

    def __init__(self, group, auto_fn=None):
        self.group = group
        self.impls = {}
        self.auto_fn = auto_fn

    def load(self, name):
        if name in self.impls:
            return self.impls[name]()
        if self.auto_fn:
            loader = self.auto_fn(name)
            if loader:
                self.impls[name] = loader
                return loader()
            try:
                import pkg_resources
            except ImportError:
                pass
        else:
            for impl in pkg_resources.iter_entry_points(
                self.group, name):
                self.impls[name] = impl.load
            return impl.load()
        raise exc.NoSuchModuleError(
        "Can't load plugin: %s:%s" % (self.group, name))

    def register(self, name, modulepath, objname):
    def load():
    mod = compat.import_(modulepath)
    for token in modulepath.split(".")[1:]:
    mod = getattr(mod, token)
    return getattr(mod, objname)
self.impls[name] = load