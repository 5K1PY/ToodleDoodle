CREATE TABLE polls (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    closed BOOLEAN NOT NULL
);

CREATE TABLE poll_options (
    id SERIAL PRIMARY KEY,
    poll_id TEXT,
    poll_option TEXT NOT NULL,
    CONSTRAINT fk_poll_id
        FOREIGN KEY (poll_id)
        REFERENCES polls(id)
            ON DELETE CASCADE
);

CREATE TABLE poll_data (
    id SERIAL PRIMARY KEY,
    poll_option_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    entry bigint NOT NULL,
    CONSTRAINT fk_poll_option_id
        FOREIGN KEY (poll_option_id)
        REFERENCES poll_options(id)
            ON DELETE CASCADE
);
