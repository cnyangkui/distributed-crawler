# -*- encoding: utf-8 -*-
from geowind_crawler import settings

def get_attr(name):
    return settings.__getattribute__(name)