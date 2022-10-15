from collections import namedtuple

# change this also in new_poll.js
DAY_INCREMENT_DEFAULT = 1
TIME_INCREMENT_DEFAULT = 60


UNKNOWN = "❔"
AVAILABLE = "✅"
UNAVAILABLE = "❌"
NOT_PREFERED = "(✔️)"

AVAILABILITY = [UNKNOWN, AVAILABLE, UNAVAILABLE, NOT_PREFERED]
DEFAULT_AVAILABILITY = UNKNOWN

# change this also in poll.js
Mode = namedtuple("Mode", ("id", "name", "key"))
MODES = {
    "": [
        Mode("transpose-tables", "Transpose tables", "t")
    ],
    "Users table": [
        Mode("interval-mode", "Interval mode", "i"),
        Mode("weights", "Weights", "w")
    ]
}