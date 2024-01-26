import sqlite3


class Database_history:
    def __init__(self):
        self.connection = sqlite3.connect('database/history.db')
        self.cur = self.connection.cursor()

    def createTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS history_id(id INTEGER PRIMARY KEY,
                                                                  history_text TEXT)''')
        self.commit()

    def addUser(self, id):
        self.cur.execute("INSERT OR REPLACE INTO history_id VALUES(?, '')", (id,))
        self.commit()

    def deleteUserHistory(self, id):
        self.cur.execute('''UPDATE history_id SET history_text = "" WHERE id = ?''', (id,))
        self.commit()

    def addHistory(self, id, text):
        self.cur.execute('UPDATE history_id SET history_text = ? WHERE id = ?', (text, id))
        self.commit()

    def getUserHistory(self, id):
        self.cur.execute('''SELECT history_text FROM history_id WHERE id = ?''', (id,))
        result = self.cur.fetchone()

        try:
            return result[0]
        except:
            return ''

    def commit(self):
        self.connection.commit()


databaseHistory = Database_history()
databaseHistory.createTable()
