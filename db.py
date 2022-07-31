import sqlite3

db = sqlite3.connect('players.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    score INT    
)""")
db.commit()


def get_min_score():
    for value in sql.execute(f"SELECT MIN(score) FROM users"):
        if value[0] is None:
            return -1
        else:
            return value[0]


def get_name_min_score(): # select name of player with min score if there are few players with that score
    for value in sql.execute(f"SELECT name, MIN(score) FROM users"):
        return value[0]


# delete one row with minimum score
def delete_min():
    sql.execute(f"DELETE FROM users WHERE score = ? AND name = ?", (get_min_score(), get_name_min_score()))
    db.commit()


def rows_count():
    return len(sql.execute("SELECT * FROM users").fetchall())


def get_all():
    return sql.execute("SELECT * FROM users").fetchall()


# check that no such name in db
def is_available(name):
    sql.execute(f"SELECT * FROM users WHERE name = ?", (name,))
    if sql.fetchone() is None:
        return True
    else:
        return False


# adds row in db if no such name and score >= min_score or rows in db < 5
def save(name, score):
    if is_available(name):
        if rows_count() >= 5:
            if score >= get_min_score():
                delete_min()
            else:
                return
        sql.execute(f"INSERT INTO users VALUES(?, ?)", (name, score))
        db.commit()



# sql.execute("DROP TABLE users")
# add("John1420", -6)
# print(get_min_score())

delete_min()

# print(count())
# add("Ma612", 100)
# # print(get_name_min_score())
x = get_all()
# x.sort(key=lambda a: a[1], reverse=True)
print(x)
