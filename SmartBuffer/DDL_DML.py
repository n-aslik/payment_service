create_history = """EATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT UNIQUE,
                is_pinned INTEGER DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """

insert_history = "INSERT OR IGNORE INTO history (content) VALUES (?)"
update_history = "UPDATE history SET is_pinned = 1 - is_pinned WHERE content = ?" 
get_history = "SELECT content, is_pinned FROM history ORDER BY is_pinned DESC, id DESC LIMIT 50"