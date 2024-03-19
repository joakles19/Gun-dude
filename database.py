import sqlite3

conn = sqlite3.connect("Gun dude database.db")
c = conn.cursor()

#Returns which levels are completed
def is_complete():
    c.execute("""SELECT completed 
              FROM level_completion""")
    conn.commit()
    return c.fetchall()

#Switches a level's state to complete
def complete_level(level):
    c.execute(f"""UPDATE level_completion 
              SET completed = 1
              WHERE level = {level}""")
    conn.commit()

#Returns which enemies feature on an inputted level
def get_enemies(level):
    c.execute(f"""SELECT * 
              FROM enemy_information
              INNER JOIN level_enemies 
              ON level_enemies.enemy = enemy_information.enemy_type AND level_enemies.level = {level}""")
    return c.fetchall()

#Returns the player's currency
def get_currency():
    c.execute("""SELECT currency
              FROM player_information
              WHERE player_id = 1""")
    return c.fetchall()[0][0]
    

#Adds to the player's currency
def add_currency(amount):
    c.execute(f"""UPDATE player_information 
              SET currency = currency + {amount}
              WHERE player_id = 1""")
    conn.commit()

def close():
    conn.close()


