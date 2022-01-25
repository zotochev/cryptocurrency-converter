import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def find_token(self, text):
        item = (text, text)
        return self.cursor.execute(
            "SELECT * FROM tokens WHERE name = ? OR symbol = ?", item
        ).fetchone()

#        if len(result) == 0:
#            return 'None' 
#        elif len(result) == 1:
#            return result[0][0]
#        else:
#            check = False
#
#            for token in result:
#                if token[1] == text or token[2] == text:
#                    return token[0]
#            return result

    def close(self):
        self.connection.close()
