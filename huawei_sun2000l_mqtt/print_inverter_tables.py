# -*- coding: utf-8 -*-

"""Pretty-print Inverter query parameters.
Grouped by measurements (inverter, panels, etc.) and by monitor group (status, wor, infor, etc.)."""

try:
    from huawei_sun2000l_mqtt.configs import config
except ModuleNotFoundError:
    print('Run setup.py first')
    exit()
from huawei_sun2000l_mqtt.lib import Huawei
from tabulate import tabulate

reg_map = Huawei.register_map
data = []
for k in reg_map.keys():
    data.append([k, reg_map[k]['name'], f"{reg_map[k]['measurement']}/{reg_map[k]['fieldname']}", reg_map[k]['units'], reg_map[k]['group']])
order_1 = ['equipment', 'info', 'monitor', 'work', 'work-extra', 'status', 'alarm', 'optimizers', '3fase', 'other']
s_order = {v: i for i, v in enumerate(order_1)}
lst_sorted_1 = sorted(data, key=lambda x: s_order[x[4]])
print(tabulate(lst_sorted_1, headers=["Field", "", "mqtt publish", "Units", "Group"], tablefmt="github"))

print()

data = []
for k in reg_map.keys():
    data.append(
        [reg_map[k]['measurement'], k, reg_map[k]['name'], f"{reg_map[k]['measurement']}/{reg_map[k]['fieldname']}",
         reg_map[k]['units'], reg_map[k]['group']])

order_2 = ['equipment', 'panels', 'inverter', 'grid', 'optimizer', 'status', 'alarm']
s_order = {v: i for i, v in enumerate(order_2)}
lst_sorted_2 = sorted(data, key=lambda x: s_order[x[0]])
print(tabulate(lst_sorted_2, headers=["", "Field", "", "mqtt publish", "Units", "Group"], tablefmt="github"))


