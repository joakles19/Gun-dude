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



def close():
    conn.close()