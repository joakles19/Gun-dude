import sqlite3

conn = sqlite3.connect("Gun dude database.db")
c = conn.cursor()

#Returns which levels are completed
def is_complete(user):
    c.execute(f"""SELECT completed 
            FROM {user}levels""")
    conn.commit()
    return c.fetchall()

#Switches a level's state to complete
def complete_level(level,user):
    c.execute(f"""UPDATE {user}levels
              SET completed = 1
              WHERE levels = ?""",str(level))
    conn.commit()

#Returns which enemies feature on an inputted level
def get_enemies(level):
    c.execute("""SELECT * 
              FROM enemy_information
              INNER JOIN level_enemies 
              ON level_enemies.enemy = enemy_information.enemy_type AND level_enemies.level = ?""",(str(level),))
    return c.fetchall()

#Returns the player's currency
def get_currency():
    c.execute("""SELECT currency
              FROM player_information
              WHERE player_id = 1""")
    return c.fetchall()[0][0]
    
#Adds to the player's currency
def add_currency(amount):
    c.execute("""UPDATE player_information 
              SET currency = currency + ?
              WHERE player_id = 1""", str(amount))
    conn.commit()

#Returns the enemy information
def enemy_information():
    c.execute("""SELECT * 
              FROM enemy_information""")
    return c.fetchall()

#Returns all usernames 
def return_usernames():
    c.execute("""SELECT *
              FROM usernames""")
    return c.fetchall()

#Adds new username
def new_username(new_name):
    c.execute("""INSERT INTO usernames
               VALUES (?,False)""",(str(new_name),))
    conn.commit()

#Deletes user
def delete_user(username):
    c.execute("""DELETE FROM usernames
               WHERE username = ?""",(str(username),))
    c.execute(f"""DROP TABLE {username}levels""")
    conn.commit()

#Choose user
def choose_user(username):
    c.execute("""UPDATE usernames 
              SET in_use = 
              (CASE WHEN username = ? THEN 1 
              ELSE 0 
              END)""",(str(username),))
    conn.commit()

#Return user
def get_user():
    c.execute("""SELECT username 
              FROM usernames 
              WHERE in_use = 1""")
    user = c.fetchone()
    if user is None:
        return 'Select/create a user to play'
    else:
        return user[0]

#Create user table
def create_tables(username):
    c.execute(f"""CREATE TABLE {username}levels(
              levels varchar,
              completed boolean)""")
    c.execute(f"""INSERT INTO {username}levels
                  VALUES(0,1)""")
    for n in range(1,11):
        c.execute(f"""INSERT INTO {username}levels
                  VALUES({n},0)""")
    conn.commit()
    
#Closes database
def close():
    conn.close()