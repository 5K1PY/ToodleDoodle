DROP TABLE polls;
DROP TABLE poll_options;
DROP TABLE poll_data;

CREATE TABLE polls (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL 
);

CREATE TABLE poll_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id TEXT,
    option TEXT NOT NULL,
    CONSTRAINT fk_poll_id
        FOREIGN KEY (poll_id)
        REFERENCES polls(id)
            ON DELETE CASCADE
);

CREATE TABLE poll_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_option_id INTEGER NOT NULL,
    user TEXT NOT NULL,
    entry INTEEGER NOT NULL,
    CONSTRAINT fk_poll_option_id
        FOREIGN KEY (poll_option_id)
        REFERENCES poll_options(id)
            ON DELETE CASCADE
);