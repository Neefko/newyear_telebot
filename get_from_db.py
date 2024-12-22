import sqlite3


class DatabaseBot:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('bot', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_user(self, id):
        self.cursor.execute('SELECT id FROM user WHERE id=?', (id,))
        return self.cursor.fetchone()

    def get_name(self, id):
        self.cursor.execute('SELECT name FROM user WHERE id = ?', (id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def get_language(self, id):
        self.cursor.execute('SELECT language FROM user WHERE id=?', (id,))
        return self.cursor.fetchone()

    def register(self, id, name, language):
        self.cursor.execute('INSERT INTO user (id, name, language) VALUES (?, ?, ?)', (id, name, language))
        self.conn.commit()
        return True
    def exam_id(self, id):
        if self.cursor.execute('SELECT id FROM user WHERE id=?',(id,)).fetchone() is None:
            return False
        else:
            return True
    def update_language(self, id, language):
        self.cursor.execute('UPDATE user SET language=? WHERE id=?', (language, id))
        self.conn.commit()
        return True