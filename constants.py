from collections import namedtuple

# change this also in new_poll.js
DAY_INCREMENT_DEFAULT = 1
TIME_INCREMENT_DEFAULT = 60

# change this also in poll.js
UNKNOWN = "❔"
AVAILABLE = "✅"
UNAVAILABLE = "❌"
NOT_PREFERRED = "(✔️)"

AVAILABILITY = [UNKNOWN, AVAILABLE, UNAVAILABLE, NOT_PREFERRED]
AVAILABILITY_WITH_TEXT = [
    (AVAILABLE, "Available"),
    (NOT_PREFERRED, "Not preferred"),
    (UNAVAILABLE, "Unavailable"),
    (UNKNOWN, "Unknown")
]

DEFAULT_AVAILABILITY = UNKNOWN

# change this also in poll.js
Mode = namedtuple("Mode", ("id", "name", "key", "description"))
MODES = {
    "": [
        Mode("transpose-tables", "Transpose tables", "t", "")
    ],
    "Users table": [
        Mode("interval-mode", "Interval mode", "i", "Change multiple days at once"),
        Mode("weights", "Weights", "w", "Set importance for each user. (Importance is only visible to you.)"),
        Mode("buttons", "Use buttons", "b", "Use select menus / buttons.")
    ]
}
