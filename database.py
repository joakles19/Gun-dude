import sqlite3

conn = sqlite3.connect("Gun dude database.db")
c = conn.cursor()

def is_complete():
    c.execute("SELECT completed FROM level_completion")
    conn.commit()
    return c.fetchall()

def complete_level(level):
    c.execute(f"""UPDATE level_completion 
              SET completed = 1
              WHERE level = {level}""")
    conn.commit()

def get_enemies(level):
    c.execute(f"""SELECT * 
              FROM enemy_information
              INNER JOIN level_enemies ON level_enemies.enemy = enemy_information.enemy_type AND level_enemies.level = {level}""")
    return c.fetchall()

def close():
    conn.close()


