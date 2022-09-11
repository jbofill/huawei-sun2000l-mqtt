* OUTDATED. MUST REWRITE!!! *

[[_TOC_]]

# EOS Huawei Sun2000 inverter MQTT

Publishing [Huawei Sun 2000l](https://support.huawei.com/enterprise/en/digital-power/sun2000l-pid-22027611) inverter information via MQTT, so it can be used by Home Assistant   

# Main process

The main process in this project is [eos_inverter_mqtt.py](https://gitlab.com/eos-solar/eos-inverter-mqtt/-/blob/main/eos_inverter_mqtt.py) that publishes MQTT responses to inverter queries.

It subscribes to topics under "sun2000l/query" and publishes inverter query results on MQTT.

For example, publishing "sun2000l/query" with value "P_daily" will make the process query inverter's daily energy yield, and publish the result in topic "panels/daily_energy".

[Field name table](#sensor-field-names) list possible query fields. 

Group queries can be made publishing "sun2000l/query" with group name "group:<group_name>". For example, "group:info" will publish "inverter/internal_temp", "panels/accum_energy" and "panels/daily_energy" results.

# Query schedule utility

[schedule_publish.py](https://gitlab.com/eos-solar/eos-inverter-mqtt/-/blob/main/schedule_publish.py) can be used to schedule periodic queries. 
Copy [config_schedule_example.py](https://gitlab.com/eos-solar/eos-inverter-mqtt/-/blob/main/config_schedule_example.py) as config_schedule.py and ajust to your needs.

Example:
'group:monitor': '1.5m' -> read every 90 seconds registers in monitor group
'group:status': '1h -> read every 1 hour registers in status group
'M_A-U': '5m' -> read register 'M_A-U' (grid voltage) every 5 ms
'group:equipment': 'once_at_start'

- units: m or h (minutes or hours)
- fraccions allowed (e.g. 1.5h)
- Minimum time: 1 minute.
- once_at_start: execute once at start of process

# Home assistant utilities

## Sensors and buttons generator
[ha_sensors_and_buttons.py](https://gitlab.com/eos-solar/eos-inverter-mqtt/-/blob/main/ha_sensors_and_buttons.py) will generate sensor and button definition that can be used by Home Assistant.
It will create a subdirectory (./sensors and ./buttons, by default) that can be included in HA configuration.yalm: 

        mqtt: 
          sensor: !include_dir_merge_list sensors/
          button: !include_dir_merge_list buttons/

It will create a sensor for each topic in [table](#sensor-field-names) column 'mqtt publish'. It creats a file for each group of sensors (equipment.yalm, monitor.yalm, etc.). For example:

        - name: "inverter_internal_temp"
          unique_id: "inverter_internal_temp"
          state_topic: "inverter/internal_temp"
          unit_of_measurement: "°C"

In the same way el will create a button definition for each group in the [table](#sensor-field-names), so that pressing de button will post groups mqtt queries. For example:

        - name: "Monitor Info"
          unique_id: "Monitor Info"
          command_topic: "sun2000l/query"
          payload_press: "group:info"


## Energy integration

Include these three sensors as energy sensors in configuration.yaml, so they can be used in HA energy integration:

        sensor:
          - platform: integration
            source: sensor.consum_de_xarxa
            name: consum_energia_xarxa
            unique_id: consum_energia_xarxa
            unit_prefix: k
            round: 2
          - platform: integration
            source: sensor.panels_active_power
            name: produccio_energia_panells
            unique_id: produccio_energia_panells
            unit_prefix: k
            round: 2
          - platform: integration
            source: sensor.excedents_a_xarxa
            name: excedents_energia_xarxa
            unique_id: excedents_energia_xarxa
            unit_prefix: k
            round: 2


![alt text](img/energy-integration.png "Title Text")


# Installation

Install git and virtualenv (Ubuntu or Debian):

    $ sudo apt-get install git virtualenv

Create user (here we use *eos*.). 

    $ sudo useradd -m -s /bin/bash eos
    $ sudo su eos
    $ cd

Download application

    $ git clone https://gitlab.com/eos-solar/eos-inverter-mqtt.git
    
Creat virtual enviroment and install requirements

    $ virtualenv --python=python3 env
    $ source env/bin/activate
    (env) $ pip install -r eos-inverter-mqtt/requirements.txt

Copy configuration file

    (env) $ cp eos-inverter-mqtt/config_example.py eos-inverter-mqtt/config.py

Update inverter ip and port

    (env) $ nano eos-inverter/config.py

Copy schedule configuration file

    (env) $ cp eos-inverter-mqtt/config_schedule_example.py eos-inverter-mqtt/config_schedule.py
    
Update schedule config to your preferences

    (env) $ nano eos-inverter/config_schedule.py


Start `eos_inverter_mqtt.py` and `schedule_publish.py` as a system services:

    $ chmod +x eos-inverter_mqtt/start_eos_service_mqtt.sh
    $ chmod +x eos-inverter_mqtt/start_schedule_publish.sh
    $ exit

    $ sudo cp /home/eos/eos-inverter-mqtt/eos_inverter_mqtt.service /etc/systemd/system/ 
    $ sudo cp /home/eos/eos-inverter-mqtt/eos_schedule.service /etc/systemd/system/
    # if you dont't use *eos* user, change username and home directori on
    #     /etc/systemd/system/eos_inverter_mqtt.service
    #     /etc/systemd/system/eos_schedule.service)

    $ sudo systemctl enable eos_inverter_mqtt
    $ sudo systemctl start eos_inverter_mqtt
    $ sudo systemctl status eos_inverter_mqtt

    $ sudo systemctl enable eos_schedule
    $ sudo systemctl start eos_schedule
    $ sudo systemctl status eos_schedule

To generate Home Assistant [sensor and button definitions](#sensors-and-buttons-generator):

    $ sudo su eos
    $ cd
    $ source env/bin/activate
    $ (env) python eos-inverter_mqtt/ha_sensors_and_buttons.py

and copy both directories to your HA config (`sensors/` and `buttons/`)


## Update application

    $ sudo su eos
    $ cd ~/eos-inverter-mqtt
    $ git pull https://gitlab.com/eos-solar/eos-inverter-mqtt
    $ exit
    $ sudo systemctl daemon-reload
    

# Query fields

## Sensor field names

Sorted by Group

| Field      | Description                      | mqtt publish            | Units | Group       |
|------------|----------------------------------|-------------------------|-------|-------------|
| Model      | Model                            | equipment/Model         |       | equipment   |
| SN         | Serial Number                    | equipment/SN            |       | equipment   |
| strings    | Number of strings                | equipment/strings       |       | equipment   |
| Pn         | Rated power                      | equipment/Pn            | kW    | equipment   |
| Pmax       | Maximum active power             | equipment/Pmax          | kW    | equipment   |
| Smax       | Maximum apparent power           | equipment/Smax          | kVA   | equipment   |
| Qmax       | Maximum reactive power to grid   | equipment/Qmax          | kVar  | equipment   |
| Qgrid      | Maximum reactive power from grid | equipment/Qgrid         | kVar  | equipment   |
| Insulation | Insulation resistance            | equipment/Insulation    | MΩ    | equipment   |
| Temp       | Internal temperature             | inverter/internal_temp  | °C    | info        |
| P_accum    | Accumulated energy yield         | panels/accum_energy     | kWh   | info        |
| P_daily    | Daily energy yield               | panels/daily_energy     | kWh   | info        |
| M_PTot     | Grid Accumulated Energy          | grid/accumulated_energy | kWh   | info        |
| P_active   | Active power                     | panels/active_power     | W[*]  | **monitor** |
| M_P        | Active Grid power (<0 obtaning)  | grid/active_power       | W     | **monitor** |
|            | Grid consumption[**]             | grid/consumption        | W     | **monitor** |
|            | Grid surplus[**]                 | grid/surplus            | W     | **monitor** |
|            | Home consumption[**]             | home/consumption        | W     | **monitor** |
| PV_P       | Input power (Input to inverter)  | panels/panel_P          | kW    | work        |
| I_A        | Phase Current A                  | panels/current_a        | A     | work        |
| PF         | Power Factor                     | panels/power_factor     |       | work        |
| η          | Efficiency                       | panels/efficiency       | %     | work        |
| M_Pr       | Active Grid reactive power       | grid/reactive_power     | VAR   | work        |
| M_A-U      | Active Grid A Voltage            | grid/voltage            | V     | work        |
| M_A-I      | Active Grid A Current            | grid/current            | I     | work        |
| M_PF       | Active Grid PF                   | grid/power_factor       |       | work        |
| M_Freq     | Active Grid Frequency            | grid/frequency          | Hz    | work        |
| M_PExp     | Grid Exported Energy             | grid/exported_energy    | kWh   | work        |
| M_A-P      | Active Grid A power              | grid/power              | W     | work        |
| PV1_U      | PV1 voltage                      | panels/panel1_V         | V     | work-extra  |
| PV1_I      | PV1 current                      | panels/panel1_I         | A     | work-extra  |
| PV2_U      | PV2 voltage                      | panels/panel2_V         | V     | work-extra  |
| PV2_I      | PV2 current                      | panels/panel2_I         | A     | work-extra  |
| U_A-B      | Line Voltage A-B                 | panels/voltage_a_b      | V     | work-extra  |
| U_A        | Phase Voltage A                  | panels/voltage_a        | V     | work-extra  |
| U_B        | Phase Voltage B                  | panels/voltage_b        | V     | work-extra  |
| P_reactive | Reactive power                   | panels/reactive_power   | kVar  | work-extra  |
| Frequency  | Grid frequency                   | panels/frequency        | Hz    | work-extra  |
| Start      | Startup time                     | inverter/Start          | s     | status      |
| Shutdown   | Shutdown time                    | inverter/Shutdown       | s     | status      |
| Time       | Current time                     | inverter/Time           | s     | status      |
| State1     | Status 1                         | status/state1           |       | status      |
| State2     | Status 2                         | status/state2           |       | status      |
| State3     | Status 3                         | status/state3           |       | status      |
| Status     | Device status                    | inverter/status         |       | status      |
| Fault      | Fault code                       | status/fault_code       |       | status      |
| P_peak     | Peak Power                       | panels/peak_power       | kW    | status      |
| Alarm1     | Alarm 1                          | alarm/alarm1            |       | alarm       |
| Alarm2     | Alarm 2                          | alarm/alarm2            |       | alarm       |
| Alarm3     | Alarm 3                          | alarm/alarm3            |       | alarm       |
| Optim_tot  | Number of optimizers             | optimizer/Optim_tot     |       | optimizers  |
| Optim_on   | Number of online optimizers      | optimizer/Optim_on      |       | optimizers  |
| Optim_opt  | Optimizer Feature data           | optimizer/Optim_opt     |       | optimizers  |
| U_B-C      | Line Voltage B-C                 | panels/voltage_b_c      | V     | 3fase       |
| U_C-A      | Line Voltage C-A                 | panels/voltage_c_a      | V     | 3fase       |
| U_C        | Phase Voltage C                  | panels/voltage_c        | V     | 3fase       |
| I_B        | Phase Current B                  | panels/current_b        | A     | 3fase       |
| I_C        | Phase Current C                  | panels/current_c        | A     | 3fase       |
| M_B-U      | Active Grid B Voltage            | grid/voltage_b          | V     | 3fase       |
| M_C-U      | Active Grid C Voltage            | grid/voltage_c          | V     | 3fase       |
| M_B-I      | Active Grid B Current            | grid/current_b          | I     | 3fase       |
| M_C-I      | Active Grid C Current            | grid/current_c          | I     | 3fase       |
| M_U_AB     | Active Grid A-B Voltage          | grid/voltage_a_b        | V     | 3fase       |
| M_U_BC     | Active Grid B-C Voltage          | grid/voltage_b_c        | V     | 3fase       |
| M_U_CA     | Active Grid C-A Voltage          | grid/voltage_c_a        | V     | 3fase       |
| M_B-P      | Active Grid B power              | grid/power_b            | W     | 3fase       |
| M_C-P      | Active Grid C power              | grid/power_c            | W     | 3fase       |

## measurement type table

Same table as previous, group by measurement type

| Type      | Field      | Description                      | mqtt publish            | Units | Group        |
|-----------|------------|----------------------------------|-------------------------|-------|--------------|
| equipment | Model      | Model                            | equipment/Model         |       | equipment    |
| equipment | SN         | Serial Number                    | equipment/SN            |       | equipment    |
| equipment | strings    | Number of strings                | equipment/strings       |       | equipment    |
| equipment | Pn         | Rated power                      | equipment/Pn            | kW    | equipment    |
| equipment | Pmax       | Maximum active power             | equipment/Pmax          | kW    | equipment    |
| equipment | Smax       | Maximum apparent power           | equipment/Smax          | kVA   | equipment    |
| equipment | Qmax       | Maximum reactive power to grid   | equipment/Qmax          | kVar  | equipment    |
| equipment | Qgrid      | Maximum reactive power from grid | equipment/Qgrid         | kVar  | equipment    |
| equipment | Insulation | Insulation resistance            | equipment/Insulation    | MΩ    | equipment    |
| panels    | PV1_U      | PV1 voltage                      | panels/panel1_V         | V     | work-extra   |
| panels    | PV1_I      | PV1 current                      | panels/panel1_I         | A     | work-extra   |
| panels    | PV2_U      | PV2 voltage                      | panels/panel2_V         | V     | work-extra   |
| panels    | PV2_I      | PV2 current                      | panels/panel2_I         | A     | work-extra   |
| panels    | PV_P       | Input power (entrada inversor)   | panels/panel_P          | kW    | work         |
| panels    | U_A-B      | Line Voltage A-B                 | panels/voltage_a_b      | V     | work-extra   |
| panels    | U_B-C      | Line Voltage B-C                 | panels/voltage_b_c      | V     | 3fase        |
| panels    | U_C-A      | Line Voltage C-A                 | panels/voltage_c_a      | V     | 3fase        |
| panels    | U_A        | Phase Voltage A                  | panels/voltage_a        | V     | work-extra   |
| panels    | U_B        | Phase Voltage B                  | panels/voltage_b        | V     | work-extra   |
| panels    | U_C        | Phase Voltage C                  | panels/voltage_c        | V     | 3fase        |
| panels    | I_A        | Phase Current A                  | panels/current_a        | A     | work         |
| panels    | I_B        | Phase Current B                  | panels/current_b        | A     | 3fase        |
| panels    | I_C        | Phase Current C                  | panels/current_c        | A     | 3fase        |
| panels    | P_peak     | Peak Power                       | panels/peak_power       | kW    | status       |
| panels    | P_active   | Active power                     | panels/active_power     | W[*]  | **monitor**  |
| panels    | P_reactive | Reactive power                   | panels/reactive_power   | kVar  | work-extra   |
| panels    | PF         | Power Factor                     | panels/power_factor     |       | work         |
| panels    | Frequency  | Grid frequency                   | panels/frequency        | Hz    | work-extra   |
| panels    | η          | Efficiency                       | panels/efficiency       | %     | work         |
| panels    | P_accum    | Accumulated energy yield         | panels/accum_energy     | kWh   | info         |
| panels    | P_daily    | Daily energy yield               | panels/daily_energy     | kWh   | info         |
| inverter  | Start      | Startup time                     | inverter/Start          | s     | status       |
| inverter  | Shutdown   | Shutdown time                    | inverter/Shutdown       | s     | status       |
| inverter  | Time       | Current time                     | inverter/Time           | s     | status       |
| inverter  | Status     | Device status                    | inverter/status         |       | status       |
| inverter  | Temp       | Internal temperature             | inverter/internal_temp  | °C    | info         |
| grid      | M_P        | Active Grid power (<0 obtaning)  | grid/active_power       | W     | **monitor**  |
| grid      |            | Grid consumption[**]             | grid/consumption        | W     | **monitor**  |
| grid      |            | Grid surplus[**]                 | grid/surplus            | W     | **monitor**  |
| grid      | M_Pr       | Active Grid reactive power       | grid/reactive_power     | VAR   | work         |
| grid      | M_A-U      | Active Grid A Voltage            | grid/voltage            | V     | work         |
| grid      | M_B-U      | Active Grid B Voltage            | grid/voltage_b          | V     | 3fase        |
| grid      | M_C-U      | Active Grid C Voltage            | grid/voltage_c          | V     | 3fase        |
| grid      | M_A-I      | Active Grid A Current            | grid/current            | I     | work         |
| grid      | M_B-I      | Active Grid B Current            | grid/current_b          | I     | 3fase        |
| grid      | M_C-I      | Active Grid C Current            | grid/current_c          | I     | 3fase        |
| grid      | M_PF       | Active Grid PF                   | grid/power_factor       |       | work         |
| grid      | M_Freq     | Active Grid Frequency            | grid/frequency          | Hz    | work         |
| grid      | M_PExp     | Grid Exported Energy             | grid/exported_energy    | kWh   | work         |
| grid      | M_U_AB     | Active Grid A-B Voltage          | grid/voltage_a_b        | V     | 3fase        |
| grid      | M_U_BC     | Active Grid B-C Voltage          | grid/voltage_b_c        | V     | 3fase        |
| grid      | M_U_CA     | Active Grid C-A Voltage          | grid/voltage_c_a        | V     | 3fase        |
| grid      | M_A-P      | Active Grid A power              | grid/power              | W     | work         |
| grid      | M_B-P      | Active Grid B power              | grid/power_b            | W     | 3fase        |
| grid      | M_C-P      | Active Grid C power              | grid/power_c            | W     | 3fase        |
| grid      | M_PTot     | Grid Accumulated Energy          | grid/accumulated_energy | kWh   | info         |
| home      |            | Home consumption[**]             | home/consumption        | W     | **monitor**  |
| optimizer | Optim_tot  | Number of optimizers             | optimizer/Optim_tot     |       | optimizers   |
| optimizer | Optim_on   | Number of online optimizers      | optimizer/Optim_on      |       | optimizers   |
| optimizer | Optim_opt  | Optimizer Feature data           | optimizer/Optim_opt     |       | optimizers   |
| status    | State1     | Status 1                         | status/state1           |       | status       |
| status    | State2     | Status 2                         | status/state2           |       | status       |
| status    | State3     | Status 3                         | status/state3           |       | status       |
| status    | Fault      | Fault code                       | status/fault_code       |       | status       |
| alarm     | Alarm1     | Alarm 1                          | alarm/alarm1            |       | alarm        |
| alarm     | Alarm2     | Alarm 2                          | alarm/alarm2            |       | alarm        |
| alarm     | Alarm3     | Alarm 3                          | alarm/alarm3            |       | alarm        |


## Notes

[*]: Inverter returns value in kW, we convert it to W

[**]: When quering "group:monitor", these 3 values are calculated from P_active and M_P values. They don't have a fieldname, so they can't be queried individualy (must use group:monitor):

        grid_consumption = 0
        grid_surplus = 0
        if response['M_P']['value'] < 0:
            grid_consumption = -response['M_P']['value']
        else:
            grid_surplus = response['M_P']['value']
        home_consumption = response['P_active']['value'] - response['M_P']['value']

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## License
For open source projects, say how it is licensed.

