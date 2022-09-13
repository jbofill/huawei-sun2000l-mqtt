# -*- coding: utf-8 -*-

"""Pretty-print Inverter query parameters.
Grouped by measurements (inverter, panels, etc.) and by monitor group (status, wor, infor, etc.)."""

try:
    from huawei_sun2000l_mqtt.configs import config
except ModuleNotFoundError:
    print('Run setup.py first')
    exit()
from huawei_sun2000l_mqtt.lib.Huawei import register_map
from tabulate import tabulate
import pandas as pd
import gettext
from huawei_sun2000l_mqtt.configs import config

language = gettext.translation('messages', localedir='i18n', languages=[config.lang])
language.install()
_ = language.gettext

df = pd.DataFrame(register_map)
t = df.transpose()
t.index.name = 'Sensor'
t['mqtt publish'] = t['measurement']+'/'+t['fieldname']
g = t.get(["description", "units", "mqtt publish", "measurement", "group"]).sort_values('group')
m = t.get(["description", "units", "mqtt publish", "measurement", "group"]).sort_values('measurement')
print()
print(_('Sorted by group'))
print(g.to_markdown())
print()
print()
print(_('Sorted by measurement'))
print(m.to_markdown())
