# -*- encoding: utf-8 -*-
from geospider import settings


def get_attr(name):
    return settings.__getattribute__(name)