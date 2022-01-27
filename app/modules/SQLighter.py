import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_all_tokens(self, text):
        return self.cursor.execute(
            "SELECT * FROM tokens"
        ).fetchall()

    def is_token_in_db(self, token):
        text = token.lower()
        item = (text, text)
        result = self.cursor.execute(
            "SELECT * FROM tokens WHERE name = ? OR symbol = ?", item
        ).fetchall()

        if len(result) == 1:
            return result[0]
        else:
            return False

    def close(self):
        self.connection.close()
