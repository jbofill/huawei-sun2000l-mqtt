import gettext
from huawei_sun2000l_mqtt.lib.Huawei import register_map as r
import pandas as pd
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator
from pprint import pprint
from huawei_sun2000l_mqtt.configs import config

language = gettext.translation('messages', localedir='i18n', languages=[config.lang])
language.install()
_ = language.gettext


def main():
    def print_schedule(sc):
        print()
        print('--------------------------------------------')
        pprint(sc, sort_dicts=False, width=1)
        print('--------------------------------------------')
        print()

    try:
        import config_schedule
    except ImportError:
        action = 'new'
    else:
        if hasattr(config_schedule, 'schedule'):
            print(_('Schedule config files exists'))
            print_schedule(config_schedule.schedule)
            action = inquirer.select(
                message="Select an action:",
                choices=[
                    Choice(name=_("Update schedule"), value='update'),
                    Choice(name=_("New schedule"), value='new'),
                    Choice(value=None, name="Exit"),
                ],
                default=1,
            ).execute()
            if not action:
                exit()
        else:
            action = 'new'

    df = pd.DataFrame(r)
    t = df.transpose()
    g = t.get(["description", "units", "measurement", "group"]).sort_values('group')
    select_group = set(g.to_dict(orient='list')['group'])
    group_choices = []
    for group in select_group:
        group_fields = g.loc[g['group'] == group].index.tolist()
        group_choices.append(Choice(group, name=f"{group}: {group_fields}"))
    sensor_choices = []
    for sensor in g.index.tolist():
        sensor_fields = g.loc[[sensor]].to_string(header=False, index=False)
        sensor_choices.append(Choice(sensor, name=f"{sensor}: {sensor_fields}"))
    if action == 'new':
        schedule = {
            # 'group:monitor': '1m',
            # 'group:work': '1h',
            # 'group:equipment': 'once_at_start',
            # 'M_A-U': '5m'
        }
    else:
        schedule = config_schedule.schedule
        print_schedule(schedule)
    while True:
        select_type = inquirer.select(
            message=_("Select:"),
            choices=[
                Choice("group", name="Group of sensors"),
                Choice("sensor", name="Individual sensor"),
                Choice(value=None, name="Exit"),
            ],
            multiselect=False,
            default=1
        ).execute()
        if not select_type:
            break
        print()
        if select_type:
            if select_type == 'group':
                selected_item = inquirer.select(
                    message="Select group:",
                    choices=group_choices,
                    wrap_lines=True,
                    # max_height=2,
                    multiselect=False,
                    border=True
                ).execute()
                print()
                print(selected_item)
                print(g.loc[g['group'] == selected_item])
                # show = inquirer.confirm(message=f"Confirm group {selected_item}?", default=True).execute()
            else:
                selected_item = inquirer.fuzzy(
                    message="Select sensor:",
                    choices=sensor_choices,
                    wrap_lines=True,
                    multiselect=False,
                ).execute()
            print()
            selected_frequency = inquirer.select(
                message="Frequency",
                choices=[Choice("m", name="Minutes"),
                         Choice("h", name="Hours"),
                         Choice("once_at_start", name="Once at start")],
                multiselect=False,
                default=1
            ).execute()
            if selected_frequency == 'once_at_start':
                selected_timing = -1
            else:
                selected_timing = '0.'
                while float(selected_timing) <= 1.:
                    if selected_frequency == 'm':
                        message = "Every minutes:"
                    else:
                        message = "Every hours:"
                        # min_allowed = 1
                    selected_timing = inquirer.number(
                        message=message,
                        float_allowed=True,
                        validate=EmptyInputValidator(),
                    ).execute()
            schedule[
                f"{'group:' if select_type == 'group' else ''}{selected_item}"
            ] = f"{selected_timing if float(selected_timing) > 0 else ''}{selected_frequency}"
            print_schedule(schedule)
    print()
    confirm = inquirer.confirm(message=_("Save schedule?"), default=True).execute()
    if confirm:
        config_path = 'config_schedule.py'
        f = open(config_path, 'w')
        f.write('schedule=')
        pprint(schedule, sort_dicts=False, width=1, stream=f)
        f.close()
        print('Config saved to', config_path)


if __name__ == "__main__":
    main()
