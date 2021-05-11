from datetime import datetime, timedelta

from mscore.utilities.couple import Couple


def get_time_list(delta_left, data_range):
    base = datetime.today() - timedelta(days=delta_left)
    date_list = []

    for x in range(data_range):
        day = base + timedelta(days=x)
        date_list.append(Couple(day.strftime("%b %d"), 'col-2'))

    date_list[delta_left].second = 'col-4'

    return date_list
