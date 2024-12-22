import sqlite3
import uuid
import json


class Link:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('bot', check_same_thread=False)
        self.cursor = self.conn.cursor()


    def generate_unique_link(self, bot_username):
        unique_id = str(uuid.uuid4())
        link = f"https://t.me/{bot_username}?start={unique_id}"
        return unique_id, link

    def save_game(self, id, creator):
        self.cursor.execute("INSERT INTO game (id, creator, participants) VALUES (?, ?, ?)",(id, creator, "[]"))
        self.conn.commit()
        return True

    def add_participants(self, unique_id, new_user):
        self.cursor.execute("SELECT participants FROM game WHERE id = ?", (unique_id,))
        row = self.cursor.fetchone()
        if row:
            if row[0]:
                participants_from_db = json.loads(row[0])
            else:
                participants_from_db = []
            if new_user not in participants_from_db:
                participants_from_db.append(new_user)
                self.cursor.execute("UPDATE game SET participants = ? WHERE id = ?",
                                    (json.dumps(participants_from_db), unique_id))
                self.conn.commit()

    def get_participants(self, unique_id):
        self.cursor.execute("SELECT participants FROM game WHERE id = ?", (unique_id,))
        row = self.cursor.fetchone()
        return json.loads(row[0])

    def info_santa_creator(self, creator):
        self.cursor.execute("SELECT id, participants FROM game WHERE creator = ?", (creator,))
        rows = self.cursor.fetchall()
        games = []
        for game_id, participants_json in rows:
            if participants_json:
                participants = json.loads(participants_json)
            else:
                participants =[]
            games.append({"id": game_id, "participants": participants})
        return games

    def info_santa_participants(self, creator):
        self.cursor.execute("SELECT id, participants FROM game WHERE creator = ?", (creator,))
        rows = self.cursor.fetchall()
        games = []
        for game_id, participants_json in rows:
            if participants_json:
                participants = json.loads(participants_json)
            else:
                participants =[]
            games.append({"id": game_id, "participants": participants})
        return games