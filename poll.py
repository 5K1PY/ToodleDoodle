import calendar
from datetime import date
import re

import datetime
from constants import AVAILABILITY, AVAILABILITY_WITH_TEXT, DEFAULT_AVAILABILITY

def gen_new_options(data):
    poll_options = []
    for option_create in data:
        day_mode = option_create['day_mode']
        day1, day2 = option_create['day1'], option_create['day2']
        day_increment = option_create['day_increment']
        time_mode = option_create['time_mode']
        time1, time2, time3 = option_create['time1'], option_create['time2'], option_create['time3']
        time_increment = option_create['time_increment']

        if day_mode == 'One day':
            day2 = day1
            day_increment = 1

        while day1 <= day2:
            if time_mode == "Whole day":
                poll_options.append(day1.strftime("%Y-%m-%d"))
            elif time_mode == "Various times":
                for time in (time1, time2, time3):
                    if time is not None:
                        poll_options.append(f'{day1.strftime("%Y-%m-%d")} {time.strftime("%H:%M")}')
            elif time_mode == "Hourly range":
                time = time1
                while time <= time2:
                    poll_options.append(f'{day1.strftime("%Y-%m-%d")} {time.strftime("%H:%M")}')
                    hours, minutes = time.hour, time.minute + time_increment
                    hours, minutes = (hours + minutes // 60), (minutes % 60)
                    if hours >= 24:
                        break
                    time = datetime.time(hours, minutes)
            day1 = day1 + datetime.timedelta(days=day_increment)

    poll_options = list(sorted(set(poll_options)))
    return poll_options

def gen_edit_options(data):
    poll_options = []
    for edit_option in data:
        day = edit_option['day']
        time = edit_option['time']
        if time is None:
            poll_options.append(f'{day.strftime("%Y-%m-%d")}')
        else:
            poll_options.append(f'{day.strftime("%Y-%m-%d")} {time.strftime("%H:%M")}')

    poll_options = list(sorted(set(poll_options)))
    return poll_options

class Option:
    def __init__(self, option_id, text):
        self.text = text
        self.option_id = option_id
        match = re.match("^(\d+)-(\d\d)-(\d\d)( \d\d:\d\d)?$", text)
        self.year, self.month, self.day, self.time = match.groups()
        self.year, self.month, self.day = map(int, (self.year, self.month, self.day))
        self.dayname = date(self.year, self.month, self.day).strftime("%a")
    
    def year_and_month(self):
        return f"{calendar.month_name[self.month]} {self.year}"

    def __str__(self):
        return self.text

    def __lt__(self, option):
        return self.text < option.text

    __repr__ = __str__


class Poll:
    def __init__(self, name, description, closed, options, users, entries):
        self.name = name
        self.description = description
        self.closed = closed
        self.options = list(map(lambda x: Option(*x), options))
        self.options.sort()
        option_key = {opt.option_id: i for i, opt in enumerate(self.options)}
        
        self.users = list(map(lambda x: x[0], users))
        user_key = {user: i for i, user in enumerate(self.users)}

        self.rows = [[user, [DEFAULT_AVAILABILITY]*(len(self.options))] for user in self.users]
        for option_id, user, entry in entries:
            self.rows[user_key[user]][1][option_key[option_id]] = AVAILABILITY[entry]
        
        if self.closed is not None:
            self.final_option_i = option_key[self.closed]
            self.final_option = self.options[self.final_option_i]

    def different_than_last(self, i):
        return (i == 0) or (self.options[i-1].year_and_month() != self.options[i].year_and_month())

    def next_year_and_month(self, i):
        for j in range(i+1, len(self.options)):
            if self.options[i].year_and_month() != self.options[j].year_and_month():
                return (j - i)
        return (len(self.options) - i)

    def remove_row(self, user):
        for i, row in enumerate(self.rows):
            if row[0] == user:
                return self.rows.pop(i)

    def gen_closed_text(self):
        lines = []
        users = {a: [] for a in AVAILABILITY}
        for row in self.rows:
            users[row[1][self.final_option_i]].append(row[0])
        for icon, description in AVAILABILITY_WITH_TEXT:
            if len(users[icon]):
                lines.append([])
                lines[-1] += [str(len(users[icon])), f' users chose {icon} {description}: ' + ', '.join(users[icon])]
        return lines