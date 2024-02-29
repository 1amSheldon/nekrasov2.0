import sqlite3


class Database_users():
    def __init__(self):
        self.connection = sqlite3.connect('database/users.db')
        self.cur = self.connection.cursor()

    def updateUser(self, id) -> bool:
        if self.cur.execute(f"SELECT model FROM login_id WHERE id = {id}").fetchone() is not None:
            return True
        self.cur.execute("INSERT INTO login_id VALUES(?, 0, 0, 0, 'Обычный', '', 0, 0, 1, 0)", (id,))
        self.commit()
        return False

    def createTable(self):
        """создание базы"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS login_id(
                                                            id INTEGER PRIMARY KEY,
                                                            subscription INTEGER,
                                                            day_left INTEGER,
                                                            role INTEGER,
                                                            role_name TEXT,
                                                            role_text TEXT, 
                                                            admin INTEGER,
                                                            model INTEGER, 
                                                            free_try INTEGER,
                                                            inDialog INTEGER DEFAULT 0)''')
        self.commit()

    def setRoleName(self, id, roleName):
        self.cur.execute('UPDATE login_id SET role_name = ? WHERE id = ?', (roleName, id,))
        self.commit()

    def getRoleName(self, id):
        return self.cur.execute(f"SELECT role_name FROM login_id WHERE id = ?", (id,)).fetchone()[0]

    def setRoleText(self, id, roleText):
        self.cur.execute('UPDATE login_id SET role_text = ? WHERE id = ?', (roleText, id,))
        self.commit()

    def getRoleText(self, id):
        return self.cur.execute(f"SELECT role_text FROM login_id WHERE id = ?", (id,)).fetchone()[0]

    def getSubscription(self, id):
        if self.cur.execute(f"SELECT subscription FROM login_id WHERE id = ?", (id,)).fetchone()[0] == 1:
            return True
        return False

    def setSubscription(self, id, subscription):
        self.cur.execute('UPDATE login_id SET subscription = ? WHERE id = ?', (subscription, id,))
        self.commit()

    def addDayLeft(self, id, months):
        self.cur.execute('UPDATE login_id SET day_left = day_left + ? WHERE id = ?', (months, id,))
        self.commit()

    def setInDialog(self, id, inDialog):
        self.cur.execute('UPDATE login_id SET inDialog = ? WHERE id = ?', (inDialog, id,))
        self.commit()

    def getInDialog(self, id):
        return bool(self.cur.execute(f"SELECT inDialog FROM login_id WHERE id = ?", (id,)).fetchone()[0])

    def getDayLeft(self, id):
        return self.cur.execute(f"SELECT day_left FROM login_id WHERE id = ?", (id,)).fetchone()[0]

    def delDayLeft(self, id):
        self.cur.execute('UPDATE login_id SET day_left = day_left - 1 WHERE id = ?', (id,))
        self.commit()

    def setRole(self, id, role):
        self.cur.execute('UPDATE login_id SET role = ? WHERE id = ?', (role, id,))
        self.commit()

    def getRole(self, id):
        return self.cur.execute(f"SELECT role FROM login_id WHERE id = ?", (id,)).fetchone()[0]

    def getUsers(self):
        self.cur.execute("SELECT id FROM login_id")
        return [row[0] for row in self.cur]

    def getSubs(self):
        self.cur.execute("SELECT id FROM login_id WHERE subscription = 1")
        return [row[0] for row in self.cur]

    def setModel(self, model, id):
        self.cur.execute('UPDATE login_id SET model = ? WHERE id = ?', (model, id,))
        self.commit()

    def getModel(self, id):
        return self.cur.execute(f"SELECT model FROM login_id WHERE id = ?", (id,)).fetchone()[0]

    def getUserFreeTry(self, id):
        if self.cur.execute(f"SELECT free_try FROM login_id WHERE id = ?",
                            (id,)).fetchone()[0] == 1:
            return True
        return False

    def delUserFreeTry(self, id):
        self.cur.execute('UPDATE login_id SET free_try = 0 WHERE id = ?', (id,))
        self.commit()

    def commit(self):
        self.connection.commit()


databaseUsers = Database_users()
databaseUsers.createTable()
