CREATE TABLE words
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    code INTEGER
);
CREATE INDEX words_code_index ON words (code);