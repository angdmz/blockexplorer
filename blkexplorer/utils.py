from constance.signals import config_updated
from django.core.exceptions import AppRegistryNotReady
from django.dispatch import receiver
from collections.abc import Mapping

registered_updaters = []


def add_updater(updater):
    registered_updaters.append(updater)


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    for updater in registered_updaters:
        updater(key, new_value)


class LazyDict(Mapping):
    def __init__(self, *args, **kw):
        self._raw_dict = dict(*args, **kw)

    def __getitem__(self, key):
        func, arg = self._raw_dict.__getitem__(key)
        return func(arg)

    def __iter__(self):
        return iter(self._raw_dict)

    def __len__(self):
        return len(self._raw_dict)


def constance_setting(setting):
    from constance import config
    try:
        return getattr(config, setting)
    except AppRegistryNotReady as arnr:
        raise Exception(str(arnr))
