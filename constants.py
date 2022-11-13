from collections import namedtuple

# change this also in new_poll.js
DAY_INCREMENT_DEFAULT = 1
TIME_INCREMENT_DEFAULT = 60

# change this also in poll.js
UNKNOWN = "❔"
AVAILABLE = "✅"
UNAVAILABLE = "❌"
NOT_PREFERED = "(✔️)"

AVAILABILITY = [UNKNOWN, AVAILABLE, UNAVAILABLE, NOT_PREFERED]
AVAILABILITY_WITH_TEXT = [
    (AVAILABLE, "Available"),
    (NOT_PREFERED, "Not prefered"),
    (UNAVAILABLE, "Unavailable"),
    (UNKNOWN, "Unknown")
]

DEFAULT_AVAILABILITY = UNKNOWN

# change this also in poll.js
Mode = namedtuple("Mode", ("id", "name", "key"))
MODES = {
    "": [
        Mode("transpose-tables", "Transpose tables", "t")
    ],
    "Users table": [
        Mode("interval-mode", "Interval mode", "i"),
        Mode("weights", "Weights", "w"),
        Mode("buttons", "Use buttons", "b")
    ]
}
