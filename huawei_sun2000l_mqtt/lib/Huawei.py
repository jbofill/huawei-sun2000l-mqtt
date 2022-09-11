# Solar Inverter Modbus Interface Definitions
# https://support.huawei.com/enterprise/en/doc/EDOC1100113918?section=k002 (page 7 - 19 and 24 - 25)
# file:///home/jordi/svn/arxiu/administracio/casa-vistaalegre/aparells/fotovoltaica/Solar Inverter Modbus Interface Definitions (V3.0).pdf

# measurements:
#  production: monitor (30 segons)
#  production: work (1 min)
#  status: alarm (5 min)
#  status: status (1h)
#  info: info (12h)
#  info: equipment (once at start nodered)
#  ignore: other, optimonitor (30 segons)
#  work (1 min)
#  alarm (5 min)
#  status (1h)
#  info (12h)
#  equipment (once at start nodered)
#  ignore: other, optimizers,  3fasemizers,  3fase
# num: number in solar invert doc
# fieldname: fieldname for influxdb, if blank uses register_map keyname

import gettext
from configs import config

language = gettext.translation('messages', localedir='i18n', languages=[config.lang])
language.install()
_ = language.gettext

monitor_types = ['measurement', 'monitor']
register_map = {
    'Model': {'num': 1, 'measurement': 'equipment', 'fieldname': 'Model', 'addr': '30000', 'registers': 15,
              'name': _('Model'), 'group': 'equipment', 'scale': 1, 'type': 'str', 'units': '', 'use': 'info',
              'method': 'hold'},
    'SN': {'num': 2, 'measurement': 'equipment', 'fieldname': 'SN', 'addr': '30015', 'registers': 10,
           'name': _('Serial Number'), 'group': 'equipment', 'scale': 1, 'type': 'str', 'units': '', 'use': 'info',
           'method': 'hold'},
    'strings': {'num': 5, 'measurement': 'equipment', 'fieldname': 'strings', 'addr': '30071', 'registers': 1,
                'name': _('Number of strings'), 'group': 'equipment', 'scale': 1, 'type': 'U16', 'units': '',
                'use': 'info', 'method': 'hold'},
    'Pn': {'num': 7, 'measurement': 'equipment', 'fieldname': 'Pn', 'addr': '30073', 'registers': 2,
           'name': _('Rated power'), 'group': 'equipment', 'scale': 1000, 'type': 'U32', 'units': 'kW', 'use': 'info',
           'method': 'hold'},
    'Pmax': {'num': 8, 'measurement': 'equipment', 'fieldname': 'Pmax', 'addr': '30075', 'registers': 2,
             'name': _('Maximum active power'), 'group': 'equipment', 'scale': 1000, 'type': 'U32', 'units': 'kW',
             'use': 'info', 'method': 'hold'},
    'Smax': {'num': 9, 'measurement': 'equipment', 'fieldname': 'Smax', 'addr': '30077', 'registers': 2,
             'name': _('Maximum apparent power'), 'group': 'equipment', 'scale': 1000, 'type': 'U32', 'units': 'kVA',
             'use': 'info', 'method': 'hold'},
    'Qmax': {'num': 10, 'measurement': 'equipment', 'fieldname': 'Qmax', 'addr': '30079', 'registers': 2,
             'name': _('Maximum reactive power to grid'), 'group': 'equipment', 'scale': 1000, 'type': 'I32',
             'units': 'kVar', 'use': 'info', 'method': 'hold'},
    'Qgrid': {'num': 11, 'measurement': 'equipment', 'fieldname': 'Qgrid', 'addr': '30081', 'registers': 2,
              'name': _('Maximum reactive power from grid'), 'group': 'equipment', 'scale': 1000, 'type': 'I32',
              'units': 'kVar', 'use': 'info', 'method': 'hold'},
    'Insulation': {'num': 43, 'measurement': 'equipment', 'fieldname': 'Insulation', 'addr': '32088', 'registers': 1,
                   'name': _('Insulation resistance'), 'group': 'equipment', 'scale': 1000, 'type': 'U16', 'units': 'MΩ',
                   'use': 'info', 'method': 'hold'},
    'Start': {'num': 46, 'measurement': 'inverter', 'fieldname': 'Start', 'addr': '32091', 'registers': 2,
              'name': _('Startup time'), 'group': 'status', 'scale': 1, 'type': 'U32', 'units': 's', 'use': 'info',
              'method': 'hold'},
    'Shutdown': {'num': 47, 'measurement': 'inverter', 'fieldname': 'Shutdown', 'addr': '32093', 'registers': 2,
                 'name': _('Shutdown time'), 'group': 'status', 'scale': 1, 'type': 'U32', 'units': 's', 'use': 'info',
                 'method': 'hold'},
    'Time': {'num': 64, 'measurement': 'inverter', 'fieldname': 'Time', 'addr': '40000', 'registers': 2,
             'name': _('Current time'), 'group': 'status', 'scale': 1, 'type': 'U32', 'units': 's', 'use': 'info',
             'method': 'hold'},
    'Optim_tot': {'num': 61, 'measurement': 'optimizer', 'fieldname': 'Optim_tot', 'addr': '37200', 'registers': 1,
                  'name': _('Number of optimizers'), 'group': 'optimizers', 'scale': 1, 'type': 'U16', 'units': '',
                  'use': 'info', 'method': 'hold'},
    'Optim_on': {'num': 62, 'measurement': 'optimizer', 'fieldname': 'Optim_on', 'addr': '37201', 'registers': 1,
                 'name': _('Number of online optimizers'), 'group': 'optimizers', 'scale': 1, 'type': 'U16', 'units': '',
                 'use': 'info', 'method': 'hold'},
    'Optim_opt': {'num': 63, 'measurement': 'optimizer', 'fieldname': 'Optim_opt', 'addr': '37202', 'registers': 1,
                  'name': _('Optimizer Feature data'), 'group': 'optimizers', 'scale': 1, 'type': 'U16', 'units': '',
                  'use': 'info', 'method': 'hold'},
    'State1': {'num': 12, 'measurement': 'status', 'fieldname': 'state1', 'addr': '32000', 'registers': 1,
               'name': _('Status 1'), 'group': 'status', 'scale': 1, 'type': 'Bit16', 'units': '', 'use': 'stat',
               'method': 'hold'},
    'State2': {'num': 13, 'measurement': 'status', 'fieldname': 'state2', 'addr': '32002', 'registers': 1,
               'name': _('Status 2'), 'group': 'status', 'scale': 1, 'type': 'Bit16', 'units': '', 'use': 'stat',
               'method': 'hold'},
    'State3': {'num': 14, 'measurement': 'status', 'fieldname': 'state3', 'addr': '32003', 'registers': 2,
               'name': _('Status 3'), 'group': 'status', 'scale': 1, 'type': 'Bit32', 'units': '', 'use': 'stat',
               'method': 'hold'},
    'Alarm1': {'num': 15, 'measurement': 'alarm', 'fieldname': 'alarm1', 'addr': '32008', 'registers': 1,
               'name': _('Alarm 1'), 'group': 'alarm', 'scale': 1, 'type': 'Bit16', 'units': '', 'use': 'stat',
               'method': 'hold'},
    'Alarm2': {'num': 16, 'measurement': 'alarm', 'fieldname': 'alarm2', 'addr': '32009', 'registers': 1,
               'name': _('Alarm 2'), 'group': 'alarm', 'scale': 1, 'type': 'Bit16', 'units': '', 'use': 'stat',
               'method': 'hold'},
    'Alarm3': {'num': 17, 'measurement': 'alarm', 'fieldname': 'alarm3', 'addr': '32010', 'registers': 1,
               'name': _('Alarm 3'), 'group': 'alarm', 'scale': 1, 'type': 'Bit16', 'units': '', 'use': 'stat',
               'method': 'hold'},
    'Status': {'num': 44, 'measurement': 'inverter', 'fieldname': 'status', 'addr': '32089', 'registers': 1,
               'name': _('Device status'), 'group': 'status', 'scale': 1, 'type': 'U16', 'units': '', 'use': 'stat',
               'method': 'hold'},
    'Fault': {'num': 45, 'measurement': 'status', 'fieldname': 'fault_code', 'addr': '32090', 'registers': 1,
              'name': _('Fault code'), 'group': 'status', 'scale': 1, 'type': 'U16', 'units': '', 'use': 'stat',
              'method': 'hold'},
    'PV1_U': {'num': 18, 'measurement': 'panels', 'fieldname': 'panel1_V', 'addr': '32016', 'registers': 1,
              'name': _('PV1 voltage'), 'group': 'work-extra', 'scale': 10, 'type': 'I16', 'units': 'V', 'use': 'mult',
              'method': 'hold'},
    'PV1_I': {'num': 19, 'measurement': 'panels', 'fieldname': 'panel1_I', 'addr': '32017', 'registers': 1,
              'name': _('PV1 current'), 'group': 'work-extra', 'scale': 100, 'type': 'I16', 'units': 'A', 'use': 'mult',
              'method': 'hold'},
    'PV2_U': {'num': 20, 'measurement': 'panels', 'fieldname': 'panel2_V', 'addr': '32018', 'registers': 1,
              'name': _('PV2 voltage'), 'group': 'work-extra', 'scale': 10, 'type': 'I16', 'units': 'V', 'use': 'mult',
              'method': 'hold'},
    'PV2_I': {'num': 21, 'measurement': 'panels', 'fieldname': 'panel2_I', 'addr': '32019', 'registers': 1,
              'name': _('PV2 current'), 'group': 'work-extra', 'scale': 100, 'type': 'I16', 'units': 'A', 'use': 'mult',
              'method': 'hold'},
    'PV_P': {'num': 26, 'measurement': 'panels', 'fieldname': 'panel_P', 'addr': '32064', 'registers': 2,
             'name': _('Input power (entrada inversor)'), 'group': 'work', 'scale': 1000, 'type': 'I32', 'units': 'kW',
             'use': 'data', 'method': 'hold'},
    'U_A-B': {'num': 27, 'measurement': 'panels', 'fieldname': 'voltage_a_b', 'addr': '32066', 'registers': 1,
              'name': _('Line Voltage A-B'), 'group': 'work-extra', 'scale': 10, 'type': 'U16', 'units': 'V',
              'use': 'data', 'method': 'hold'},
    'U_B-C': {'num': 28, 'measurement': 'panels', 'fieldname': 'voltage_b_c', 'addr': '32067', 'registers': 1,
              'name': _('Line Voltage B-C'), 'group': '3fase', 'scale': 10, 'type': 'U16', 'units': 'V', 'use': 'ext',
              'method': 'hold'},
    'U_C-A': {'num': 29, 'measurement': 'panels', 'fieldname': 'voltage_c_a', 'addr': '32068', 'registers': 1,
              'name': _('Line Voltage C-A'), 'group': '3fase', 'scale': 10, 'type': 'U16', 'units': 'V', 'use': 'ext',
              'method': 'hold'},
    'U_A': {'num': 30, 'measurement': 'panels', 'fieldname': 'voltage_a', 'addr': '32069', 'registers': 1,
            'name': _('Phase Voltage A'), 'group': 'work-extra', 'scale': 10, 'type': 'U16', 'units': 'V', 'use': 'data',
            'method': 'hold'},
    'U_B': {'num': 31, 'measurement': 'panels', 'fieldname': 'voltage_b', 'addr': '32070', 'registers': 1,
            'name': _('Phase Voltage B'), 'group': 'work-extra', 'scale': 10, 'type': 'U16', 'units': 'V', 'use': 'data',
            'method': 'hold'},
    'U_C': {'num': 32, 'measurement': 'panels', 'fieldname': 'voltage_c', 'addr': '32071', 'registers': 1,
            'name': _('Phase Voltage C'), 'group': '3fase', 'scale': 10, 'type': 'U16', 'units': 'V', 'use': 'ext',
            'method': 'hold'},
    'I_A': {'num': 33, 'measurement': 'panels', 'fieldname': 'current_a', 'addr': '32072', 'registers': 2,
            'name': _('Phase Current A'), 'group': 'work', 'scale': 1000, 'type': 'I32', 'units': 'A', 'use': 'data',
            'method': 'hold'},
    'I_B': {'num': 34, 'measurement': 'panels', 'fieldname': 'current_b', 'addr': '32074', 'registers': 2,
            'name': _('Phase Current B'), 'group': '3fase', 'scale': 1000, 'type': 'I32', 'units': 'A', 'use': 'ext',
            'method': 'hold'},
    'I_C': {'num': 34, 'measurement': 'panels', 'fieldname': 'current_c', 'addr': '32076', 'registers': 2,
            'name': _('Phase Current C'), 'group': '3fase', 'scale': 1000, 'type': 'I32', 'units': 'A', 'use': 'ext',
            'method': 'hold'},
    'P_peak': {'num': 36, 'measurement': 'panels', 'fieldname': 'peak_power', 'addr': '32078', 'registers': 2,
               'name': _('Peak Power'), 'group': 'status', 'scale': 1000, 'type': 'I32', 'units': 'kW', 'use': 'data',
               'method': 'hold'},
    'P_active': {'num': 37, 'measurement': 'panels', 'fieldname': 'active_power', 'addr': '32080', 'registers': 2,
                 'name': _('Active power'), 'group': 'monitor', 'scale': 1000, 'type': 'I32', 'units': 'kW', 'use': 'data',
                 'method': 'hold'},
    'P_reactive': {'num': 38, 'measurement': 'panels', 'fieldname': 'reactive_power', 'addr': '32082', 'registers': 2,
                   'name': _('Reactive power'), 'group': 'work-extra', 'scale': 1000, 'type': 'I32', 'units': 'kVar',
                   'use': 'data', 'method': 'hold'},
    'PF': {'num': 39, 'measurement': 'panels', 'fieldname': 'power_factor', 'addr': '32084', 'registers': 1,
           'name': _('Power Factor'), 'group': 'work', 'scale': 1000, 'type': 'I16', 'units': '', 'use': 'data',
           'method': 'hold'},
    'Frequency': {'num': 40, 'measurement': 'panels', 'fieldname': 'frequency', 'addr': '32085', 'registers': 1,
                  'name': _('Grid frequency'), 'group': 'work-extra', 'scale': 100, 'type': 'U16', 'units': 'Hz',
                  'use': 'data', 'method': 'hold'},
    'η': {'num': 41, 'measurement': 'panels', 'fieldname': 'efficiency', 'addr': '32086', 'registers': 1,
          'name': _('Efficiency'), 'group': 'work', 'scale': 100, 'type': 'U16', 'units': '%', 'use': 'data',
          'method': 'hold'},
    'Temp': {'num': 42, 'measurement': 'inverter', 'fieldname': 'internal_temp', 'addr': '32087', 'registers': 1,
             'name': _('Internal temperature'), 'group': 'info', 'scale': 10, 'type': 'I16', 'units': '°C', 'use': 'data',
             'method': 'hold'},
    'P_accum': {'num': 48, 'measurement': 'panels', 'fieldname': 'accum_energy', 'addr': '32106', 'registers': 2,
                'name': _('Accumulated energy yield'), 'group': 'info', 'scale': 100, 'type': 'U32', 'units': 'kWh',
                'use': 'data', 'method': 'hold'},
    'P_daily': {'num': 49, 'measurement': 'panels', 'fieldname': 'daily_energy', 'addr': '32114', 'registers': 2,
                'name': _('Daily energy yield'), 'group': 'info', 'scale': 100, 'type': 'U32', 'units': 'kWh',
                'use': 'data', 'method': 'hold'},
    'M_P': {'num': 60, 'measurement': 'grid', 'fieldname': 'active_power', 'addr': '37113', 'registers': 2,
            'name': _('Active Grid power (<0 obtaning)'), 'group': 'monitor', 'scale': 1, 'type': 'I32', 'units': 'W',
            'use': 'data', 'method': 'hold'},
    'M_Pr': {'num': 0, 'measurement': 'grid', 'fieldname': 'reactive_power', 'addr': '37115', 'registers': 2,
             'name': _('Active Grid reactive power'), 'group': 'work', 'scale': 1, 'type': 'I32', 'units': 'VAR',
             'use': 'data', 'method': 'hold'},
    'M_A-U': {'num': 2, 'measurement': 'grid', 'fieldname': 'voltage', 'addr': '37101', 'registers': 2,
              'name': _('Active Grid A Voltage'), 'group': 'work', 'scale': 10, 'type': 'I32', 'units': 'V', 'use': 'data',
              'method': 'hold'},
    'M_B-U': {'num': 0, 'measurement': 'grid', 'fieldname': 'voltage_b', 'addr': '37103', 'registers': 2,
              'name': _('Active Grid B Voltage'), 'group': '3fase', 'scale': 10, 'type': 'I32', 'units': 'V',
              'use': 'data', 'method': 'hold'},
    'M_C-U': {'num': 0, 'measurement': 'grid', 'fieldname': 'voltage_c', 'addr': '37105', 'registers': 2,
              'name': _('Active Grid C Voltage'), 'group': '3fase', 'scale': 10, 'type': 'I32', 'units': 'V',
              'use': 'data', 'method': 'hold'},
    'M_A-I': {'num': 0, 'measurement': 'grid', 'fieldname': 'current', 'addr': '37107', 'registers': 2,
              'name': _('Active Grid A Current'), 'group': 'work', 'scale': 100, 'type': 'I32', 'units': 'I',
              'use': 'data', 'method': 'hold'},
    'M_B-I': {'num': 0, 'measurement': 'grid', 'fieldname': 'current_b', 'addr': '37109', 'registers': 2,
              'name': _('Active Grid B Current'), 'group': '3fase', 'scale': 100, 'type': 'I32', 'units': 'I',
              'use': 'data', 'method': 'hold'},
    'M_C-I': {'num': 0, 'measurement': 'grid', 'fieldname': 'current_c', 'addr': '37111', 'registers': 2,
              'name': _('Active Grid C Current'), 'group': '3fase', 'scale': 100, 'type': 'I32', 'units': 'I',
              'use': 'data', 'method': 'hold'},
    'M_PF': {'num': 0, 'measurement': 'grid', 'fieldname': 'power_factor', 'addr': '37117', 'registers': 1,
             'name': _('Active Grid PF'), 'group': 'work', 'scale': 1000, 'type': 'I16', 'units': '', 'use': 'data',
             'method': 'hold'},
    'M_Freq': {'num': 0, 'measurement': 'grid', 'fieldname': 'frequency', 'addr': '37118', 'registers': 1,
               'name': _('Active Grid Frequency'), 'group': 'work', 'scale': 100, 'type': 'I16', 'units': 'Hz',
               'use': 'data', 'method': 'hold'},
    'M_PExp': {'num': 12, 'measurement': 'grid', 'fieldname': 'exported_energy', 'addr': '37119', 'registers': 2,
               'name': _('Grid Accumulated Exported Energy'), 'group': 'work', 'scale': 100, 'type': 'I32', 'units': 'kWh',
               'use': 'data', 'method': 'hold'},
    'M_U_AB': {'num': 0, 'measurement': 'grid', 'fieldname': 'voltage_a_b', 'addr': '37126', 'registers': 2,
               'name': _('Active Grid A-B Voltage'), 'group': '3fase', 'scale': 10, 'type': 'I32', 'units': 'V',
               'use': 'data', 'method': 'hold'},
    'M_U_BC': {'num': 0, 'measurement': 'grid', 'fieldname': 'voltage_b_c', 'addr': '37128', 'registers': 2,
               'name': _('Active Grid B-C Voltage'), 'group': '3fase', 'scale': 10, 'type': 'I32', 'units': 'V',
               'use': 'data', 'method': 'hold'},
    'M_U_CA': {'num': 0, 'measurement': 'grid', 'fieldname': 'voltage_c_a', 'addr': '37130', 'registers': 2,
               'name': _('Active Grid C-A Voltage'), 'group': '3fase', 'scale': 10, 'type': 'I32', 'units': 'V',
               'use': 'data', 'method': 'hold'},
    'M_A-P': {'num': 0, 'measurement': 'grid', 'fieldname': 'power', 'addr': '37132', 'registers': 2,
              'name': _('Active Grid A power'), 'group': 'work', 'scale': 1, 'type': 'I32', 'units': 'W', 'use': 'data',
              'method': 'hold'},
    'M_B-P': {'num': 0, 'measurement': 'grid', 'fieldname': 'power_b', 'addr': '37134', 'registers': 2,
              'name': _('Active Grid B power'), 'group': '3fase', 'scale': 1, 'type': 'I32', 'units': 'W', 'use': 'data',
              'method': 'hold'},
    'M_C-P': {'num': 0, 'measurement': 'grid', 'fieldname': 'power_c', 'addr': '37136', 'registers': 2,
              'name': _('Active Grid C power'), 'group': '3fase', 'scale': 1, 'type': 'I32', 'units': 'W', 'use': 'data',
              'method': 'hold'},
    'M_PTot': {'num': 13, 'measurement': 'grid', 'fieldname': 'accumulated_energy', 'addr': '37121', 'registers': 2,
               'name': _('Grid Accumulated Energy'), 'group': 'info', 'scale': 100, 'type': 'U32', 'units': 'kWh',
               'use': 'data', 'method': 'hold'}
}

status_map = {
    0x0000: 'Standby: initializing',
    0x0001: 'Standby: detecting insulation resistance',
    0x0002: 'Standby: detecting irradiation',
    0x0003: 'Standby: grid detecting',
    0x0100: 'Starting',
    0x0200: 'On-grid (Off-grid mode: running)',
    0x0201: 'Grid connection: power limited (Off-grid mode: running: power limited)',
    0x0202: 'Grid connection: self-derating (Off-grid mode: running: self-derating)',
    0x0300: 'Shutdown: fault',
    0x0301: 'Shutdown: command',
    0x0302: 'Shutdown: OVGR',
    0x0303: 'Shutdown: communication disconnected',
    0x0304: 'Shutdown: power limited',
    0x0305: 'Shutdown: manual startup required',
    0x0306: 'Shutdown: DC switches disconnected',
    0x0307: 'Shutdown: rapid cutoff',
    0x0308: 'Shutdown: input underpowered',
    0x0401: 'Grid scheduling: cos F-P curve',
    0x0402: 'Grid scheduling: Q-U curve',
    0x0403: 'Grid scheduling: PF-U curve',
    0x0404: 'Grid scheduling: dry contact',
    0x0405: 'Grid scheduling: Q-P curve',
    0x0500: 'Spot-check ready',
    0x0501: 'Spot-checking',
    0x0600: 'Inspecting',
    0x0700: 'AFCI self check',
    0x0800: 'I-V scanning',
    0x0900: 'DC input detection',
    0x0a00: 'Running: off-grid charging',
    0xa000: 'Standby: no irradiation'
}


def test_bit(n, b):
    n &= (1 << b)
    n = (n == (1 << b))
    return n


def status(register, value):
    s = ""
    value = int(value)
    if register == 'State1':
        if test_bit(value, 0):
            s += 'standby | '
        if test_bit(value, 1):
            s += 'grid-connected | '
        if test_bit(value, 2):
            s += 'grid-connected normally | '
        if test_bit(value, 3):
            s += 'connection with derating due to power rationing | '
        if test_bit(value, 4):
            s += 'grid connection with derating due to internal causes of the solar inverter | '
        if test_bit(value, 5):
            s += 'normal stop | '
        if test_bit(value, 6):
            s += 'stop due to faults | '
        if test_bit(value, 7):
            s += 'stop due to power rationing | '
        if test_bit(value, 8):
            s += 'shutdown | '
        if test_bit(value, 9):
            s += 'spot check '
    elif register == 'State2':
        if test_bit(value, 0):
            s += 'unlocked | '
        else:
            s += 'locked | '
        if test_bit(value, 1):
            s += 'connected | '
        else:
            s += 'disconnected | '
        if test_bit(value, 2):
            s += 'DSP collecting | '
        else:
            s += 'DSP not collecting | '

    elif register == 'State3':
        if test_bit(value, 0):
            s += 'off-grid | '
        else:
            s += 'on-grid | '
        if test_bit(value, 1):
            s += 'off-grid switch enable | '
        else:
            s += 'off-grid switch disable | '

    elif register == 'Alarm1':
        if test_bit(value, 0):
            s += 'High String Input Voltage | '
        if test_bit(value, 1):
            s += 'DC Arc Fault | '
        if test_bit(value, 2):
            s += 'String Reverse Connection | '
        if test_bit(value, 3):
            s += 'String Current Backfeed | '
        if test_bit(value, 4):
            s += 'Abnormal String Power | '
        if test_bit(value, 5):
            s += 'AFCI Self-Check Fail | '
        if test_bit(value, 6):
            s += 'Phase Wire Short-Circuited to PE | '
        if test_bit(value, 7):
            s += 'Grid Loss | '
        if test_bit(value, 8):
            s += 'Grid Under voltage | '
        if test_bit(value, 9):
            s += 'Grid Over-voltage | '
        if test_bit(value, 10):
            s += 'Grid Volt. Imbalance | '
        if test_bit(value, 11):
            s += 'Grid Over-frequency | '
        if test_bit(value, 12):
            s += 'Grid Under frequency | '
        if test_bit(value, 13):
            s += 'Unstable Grid Frequency | '
        if test_bit(value, 14):
            s += 'Output Over-current | '
        if test_bit(value, 15):
            s += 'Output DC Component Over-high | '

    elif register == 'Alarm2':
        if test_bit(value, 0):
            s += 'Abnormal Residual Current | '
        if test_bit(value, 1):
            s += 'Abnormal Grounding | '
        if test_bit(value, 2):
            s += 'Low Insulation Resistance | '
        if test_bit(value, 3):
            s += 'Over temperature | '
        if test_bit(value, 4):
            s += 'Device Fault | '
        if test_bit(value, 5):
            s += 'Upgrade Failed or Version Mismatch | '
        if test_bit(value, 6):
            s += 'License Expired | '
        if test_bit(value, 7):
            s += 'Faulty Monitoring Unit | '
        if test_bit(value, 8):
            s += 'Faulty Power Collector | '
        if test_bit(value, 9):
            s += 'Battery abnormal | '
        if test_bit(value, 10):
            s += 'Active Islanding | '
        if test_bit(value, 11):
            s += 'Passive Islanding | '
        if test_bit(value, 12):
            s += 'Transient AC Over-voltage | '
        if test_bit(value, 13):
            s += 'Peripheral port short circuit | '
        if test_bit(value, 14):
            s += 'Churn output overload | '
        if test_bit(value, 15):
            s += 'Abnormal PV module configuration | '

    elif register == 'Alarm3':
        if test_bit(value, 0):
            s += 'Optimizer fault | '
        if test_bit(value, 1):
            s += 'Built-in PID operation abnormal | '
        if test_bit(value, 2):
            s += 'High input string voltage to ground | '
        if test_bit(value, 3):
            s += 'External Fan Abnormal | '
        if test_bit(value, 4):
            s += 'Battery Reverse Connection | '
        if test_bit(value, 5):
            s += 'On-grid/Off-grid controller abnormal | '
        if test_bit(value, 6):
            s += 'PV String Loss | '
        if test_bit(value, 7):
            s += 'Internal Fan Abnormal | '
        if test_bit(value, 8):
            s += 'DC Protection Unit Abnormal | '

    elif register == 'Status':
        s = status_map[value]
    elif register == 'Fault':
        s = str(value)
    else:
        s = 'invalid status'
    if s.endswith(' | '):
        s = s[:-3]
    return s
