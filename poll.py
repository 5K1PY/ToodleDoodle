import calendar
from datetime import date
import re

from constants import AVAILABILTY

class Option:
    def __init__(self, option_id, text):
        self.text = text
        self.option_id = option_id
        match = re.match("^(\d\d\d\d)-(\d\d)-(\d\d)( \d\d:\d\d)?$", text)
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
    def __init__(self, name, options, users, entries):
        self.name = name
        self.options = list(map(lambda x: Option(*x), options))
        self.options.sort()
        option_key = {opt.option_id: i for i, opt in enumerate(self.options)}
        
        self.users = list(map(lambda x: x[0], users))
        user_key = {user: i for i, user in enumerate(self.users)}

        self.rows = [[user] + [None]*(len(self.options)) for user in self.users]
        for option_id, user, entry in entries:
            self.rows[user_key[user]][option_key[option_id]+1
            ] = AVAILABILTY[entry]
    
    def diffrent_than_last(self, i):
        return (i == 0) or (self.options[i-1].year_and_month() != self.options[i].year_and_month())

    def next_year_and_month(self, i):
        for j in range(i+1, len(self.options)):
            if self.options[i].year_and_month() != self.options[j].year_and_month():
                return (j - i)
        return (len(self.options) - i)