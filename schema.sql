CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('start','cut'))
);

-- Date-based checks (history-ready)
-- check_date stored as ISO text: "YYYY-MM-DD"
CREATE TABLE IF NOT EXISTS checks (
    habit_id INTEGER NOT NULL,
    check_date TEXT NOT NULL,
    done INTEGER NOT NULL CHECK(done IN (0,1)),
    PRIMARY KEY (habit_id, check_date),
    FOREIGN KEY (habit_id) REFERENCES habits(id)
);