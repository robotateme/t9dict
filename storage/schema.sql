CREATE TABLE words
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    code TEXT
);
CREATE INDEX words_code_index ON words (code);