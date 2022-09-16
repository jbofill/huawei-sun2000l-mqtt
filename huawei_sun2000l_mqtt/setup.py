import ipaddress
import locale
import gettext
from langcodes import closest_supported_match
from os import path
import os
localedir = os.path.join(os.path.dirname(__file__), "i18n")
langs = ['ca', 'es', 'en']
current_locale, encoding = locale.getdefaultlocale()
use_lang = closest_supported_match(current_locale, langs)
if not use_lang:
    use_lang = 'en'
language = gettext.translation('messages', localedir=localedir, languages=[use_lang], fallback=True)
language.install()
_ = language.gettext

try:
    from huawei_sun2000l_mqtt.configs import config
except ImportError:
    pass
else:
    print(_('Config files exists'))
    rewrite = input(_('Rewrite? [y/N] '))
    if not rewrite.lower() in ['y', 'yes']:
        exit()


default_lang = ''
if use_lang in langs:
    default_lang = use_lang
lang = ''
while not lang:
    lang_input = input(_('Language ') + f'{langs}? [{default_lang}] ')
    if lang_input and lang_input in langs:
        lang = lang_input
    elif default_lang and not lang_input:
        lang = default_lang

# inverter_ip_default = '192.168.1.97'
inverter_ip = ''
while not inverter_ip:
    inverter_ip_input = input(_('Inverter ip? '))
    if inverter_ip_input:
        try:
            inverter_ip = ipaddress.ip_address(inverter_ip_input)
        except ValueError:
            print(_('address is invalid: %s') % inverter_ip_input)

inverter_port = ''
inverter_port_default = 502

while not inverter_port:
    inverter_ip_input = input(_('Inverter port? ') + f'[{inverter_port_default}] ')
    if inverter_ip_input:
        if inverter_ip_input.isnumeric():
            inverter_port = inverter_ip_input
        else:
            print(_('Not a number'))
    else:
        inverter_port = inverter_port_default

timeout = 3  # seconds
slave = 0x00  # unit_id. Sun2000l only responds to unit_id zero
model = "Huawei"  # do not change. It points to configs/Huawei.py

file_path = path.dirname(path.realpath(__file__))
config_file = file_path+'/configs/config.py'
c = open(config_file, 'w')
c.write(f'lang="{lang}"  # "ca", "es", "en"\n')
c.write(f'inverter_ip="{inverter_ip}"\n')
c.write(f'inverter_port={inverter_port}\n')
c.write(f'timeout={timeout}  # seconds\n')
c.write(f'slave={slave}  # unit_id. Sun2000l only responds to unit_id zero\n')
print(_('New config file created --> ')+config_file)
c.close()
