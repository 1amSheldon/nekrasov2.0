import sqlite3


class Database_statictic():
    def __init__(self):
        self.connection = sqlite3.connect('database/statistic.db')
        self.cur = self.connection.cursor()

    def createTable(self):
        """создание базы"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS data(
                                                            free_try INTEGER,
                                                            buyers INTEGER,
                                                            support_questions INTEGER, 
                                                            users INTEGER,
                                                            posts INTEGER)''')
        self.commit()
        if self.cur.execute(f"SELECT free_try FROM data").fetchone() is not None:
            return
        self.cur.execute("INSERT INTO data VALUES(0, 0, 0, 0, 0)")
        self.commit()

    def addFreeTry(self):
        self.cur.execute('UPDATE data SET free_try = free_try + 1')
        self.commit()

    def getFreeTry(self):
        return self.cur.execute(f"SELECT free_try FROM data").fetchone()[0]

    def addBuyer(self):
        self.cur.execute('UPDATE data SET buyers = buyers + 1')
        self.commit()

    def getBuyers(self):
        return self.cur.execute(f"SELECT buyers FROM data").fetchone()[0]

    def addSupportQuestion(self):
        self.cur.execute('UPDATE data SET support_questions = support_questions + 1')
        self.commit()

    def getSupportQuestions(self):
        return self.cur.execute(f"SELECT support_questions FROM data").fetchone()[0]

    def addPost(self):
        self.cur.execute('UPDATE data SET posts = posts + 1')
        self.commit()

    def getPosts(self):
        return self.cur.execute(f"SELECT posts FROM data").fetchone()[0]

    def addUsers(self):
        self.cur.execute('UPDATE data SET users = users + 1')
        self.commit()

    def getUsers(self):
        return self.cur.execute(f"SELECT users FROM data").fetchone()[0]

    def commit(self):
        self.connection.commit()


databaseStatistics = Database_statictic()
databaseStatistics.createTable()
