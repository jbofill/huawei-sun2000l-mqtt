import os
import gettext
try:
    from huawei_sun2000l_mqtt.configs import config
except ModuleNotFoundError:
    print('Run setup.py first')
    exit()
from huawei_sun2000l_mqtt.lib import Huawei

language = gettext.translation('messages', localedir='i18n', languages=[config.lang])
language.install()
_ = language.gettext

# inverter_file = config.model
# inverter_interface_definitions = __import__(inverter_file)
# reg_map = inverter_interface_definitions.register_map
reg_map = Huawei.register_map
data = []
for k in reg_map.keys():
    data.append([k, reg_map[k]['measurement'], reg_map[k]['fieldname'], reg_map[k]['description'], f"{reg_map[k]['measurement']}/{reg_map[k]['fieldname']}", reg_map[k]['units'],
                 reg_map[k]['num'], reg_map[k]['group']])

order_3 = ['equipment', 'info', 'monitor', 'work', 'work-extra', 'status', 'alarm', 'optimizers', '3fase', 'other']
s_order = {v: i for i, v in enumerate(order_3)}
lst_sorted_3 = sorted(data, key=lambda x: s_order[x[7]])

dir_sensors = input('Sensors definition directory? [sensors]')
out_dir_sensors = dir_sensors
if not dir_sensors:
    out_dir_sensors = 'sensors'
if not os.path.isdir(out_dir_sensors):
    os.makedirs(out_dir_sensors)
file = ''
out = None
name1 = _("Grid consumption")
monitor_add = f'''
- name: "{name1}"
  unique_id: "{name1}"
  state_topic: "grid/consumption"
  unit_of_measurement: "W"
  state_class: "measurement"
  device_class: "power"
- name: "Excedents a Xarxa"
  unique_id: "Excedents a Xarxa"
  state_topic: "grid/surplus"
  unit_of_measurement: "W"
  state_class: "measurement"
  device_class: "power"
- name: "Consum Casa"
  unique_id: "Consum Casa"
  state_topic: "home/consumption"
  unit_of_measurement: "W"
  state_class: "measurement"
  device_class: "power"
'''
for sensor in lst_sorted_3:
    if sensor[7] != file:
        if out:
            out.close()
        file = sensor[7]
        out = open(f"{out_dir_sensors}/{file}.yaml", 'w')
        if file == 'monitor':
            out.write(monitor_add)
    out.write(f'- name: "{sensor[1]}_{sensor[2]}"\n')
    out.write(f'  unique_id: "{sensor[1]}_{sensor[2]}"\n')
    out.write(f'  state_topic: "{sensor[4]}"\n')
    if sensor[5]:
        if sensor[0] == 'P_active':
            sensor[5] = 'W'  # eos_inverter_mqtt.py converts P_active from kW to W
        out.write(f'  unit_of_measurement: "{sensor[5]}"\n')
    if sensor[7] == 'monitor':
        out.write(f'  state_class: "measurement"\n')
        if sensor[5] == "kWh":
            out.write(f'  device_class: "energy"\n')
        else:
            out.write(f'  device_class: "power"\n')
out.close()
print(out_dir_sensors)
print(os.listdir(out_dir_sensors))
print()

dir_buttons = input('Buttons definition directory? [buttons]')
out_dir_buttons = dir_buttons
if not dir_buttons:
    out_dir_buttons = 'buttons'
if not os.path.isdir(out_dir_buttons):
    os.makedirs(out_dir_buttons)
file = ''
out = None
for group in order_3:
    if group != file:
        if out:
            out.close()
        file = group
        out = open(f"{out_dir_buttons}/{file}.yaml", 'w')
    out.write(f'- name: "Monitor {group.capitalize()}"\n')
    out.write(f'  unique_id: "Monitor {group.capitalize()}"\n')
    out.write(f'  command_topic: "sun2000l/query"\n')
    out.write(f'  payload_press: "group:{group}"\n')

print(out_dir_buttons)
print(os.listdir(out_dir_buttons))
print()
print()
print(f'''
In file configurations.yalm include

mqtt: 
  sensor: !include_dir_merge_list {out_dir_sensors}/
  button: !include_dir_merge_list {out_dir_buttons}/
''')
