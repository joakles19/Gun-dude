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
              WHERE levels = ?""",(str(level),))
    conn.commit()

#Returns which enemies feature on an inputted level
def get_enemies(level):
    c.execute("""SELECT * 
              FROM enemy_information
              INNER JOIN level_enemies 
              ON level_enemies.enemy = enemy_information.enemy_type AND level_enemies.level = ?""",(str(level),))
    return c.fetchall()

#Returns enemy_information
def enemy_information(enemy):
    c.execute("""SELECT *
              FROM enemy_information
              WHERE enemy_type = ?""",(str(enemy),))
    return c.fetchone()

#Returns boss_information
def boss_information(boss):
    c.execute("""SELECT * 
              FROM enemy_information 
              JOIN boss_information 
              ON enemy_information.enemy_type = boss_information.boss and boss_information.boss = ?""",(str(boss),))
    return c.fetchone()

#Returns the player's currency
def get_currency():
    c.execute("""SELECT currency
              FROM usernames
              WHERE in_use = 1""")
    return c.fetchall()[0][0]
    
#Adds to the player's currency
def add_currency(amount):
    c.execute(f"""UPDATE usernames 
              SET currency = currency + ?
              WHERE in_use = 1""", (str(amount),))
    conn.commit()

#Returns all usernames 
def return_usernames():
    c.execute("""SELECT *
              FROM usernames""")
    return c.fetchall()

#Adds new username
def new_username(new_name):
    c.execute("""INSERT INTO usernames
               VALUES (?,False,0)""",(str(new_name),))
    conn.commit()

#Deletes user
def delete_user(username):
    c.execute("""DELETE FROM usernames
               WHERE username = ?""",(str(username),))
    c.execute(f"""DROP TABLE {username}levels""")
    c.execute(f"""DROP TABLE {username}skills""")
    c.execute(f"""DROP TABLE {username}skins""")
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
    for n in range(1,13):
        c.execute(f"""INSERT INTO {username}levels
                  VALUES({n},0)""")
    c.execute(f"""CREATE TABLE {username}skills(
              skill varchar,
              purchased boolean)""")
    for n in range(1,16):
        c.execute(f"""INSERT INTO {username}skills
                   VALUES(?,0)""",(str(n),))
    c.execute(f"""CREATE TABLE {username}skins(
              skin varchar,
              purchased boolean,
              selected boolean)""")
    c.execute(f"""INSERT INTO {username}skins
                  VALUES('',1,1)""")
    color_list = ['Green','Grey','Orange','Purple','Black','Naked','Gman']
    for color in color_list:
        c.execute(f"""INSERT INTO {username}skins
                  VALUES(?,0,0)""",(str(color),))
    conn.commit()

#Purchase skill
def purchase_skill(skill):
    c.execute("""SELECT username FROM usernames
              WHERE in_use = 1""")
    user = c.fetchone()[0]
    c.execute(f"""UPDATE {user}skills
              SET purchased = 1
              WHERE skill = ?""",(str(skill),))
    conn.commit()

#Return skills
def get_skills():
    c.execute("""SELECT username FROM usernames
              WHERE in_use = 1""")
    user = c.fetchone()[0]
    c.execute(f"""SELECT skill FROM {user}skills
              WHERE purchased = 1""")
    return c.fetchall()
    
#Return skins
def is_skin_puchased(skin):
    c.execute("""SELECT username FROM usernames
              WHERE in_use = 1""")
    user = c.fetchone()[0]
    c.execute(f"""SELECT purchased FROM {user}skins
              WHERE skin = ?""",(str(skin),))
    return c.fetchone()[0]

def get_selected_skin():
    c.execute("""SELECT username FROM usernames
              WHERE in_use = 1""")
    user = c.fetchone()[0]
    c.execute(f"""SELECT skin FROM {user}skins
              WHERE selected = 1""")
    skin = c.fetchone()
    if skin is None:
        return ""
    else:
        return skin[0]

#Select/purchase skin
def select_skin(skin,select,purchase):
    c.execute("""SELECT username FROM usernames
              WHERE in_use = 1""")
    user = c.fetchone()[0]
    if select:
        c.execute(f"""UPDATE {user}skins
                SET selected = 
                (CASE WHEN skin = ? THEN 1 
                ELSE 0 
                END)""",(str(skin),))
    if purchase:
        c.execute(f"""UPDATE {user}skins
                  SET purchased = 1
                  WHERE skin = ?""",(str(skin),))
    conn.commit()



#Closes database
def close():
    conn.close()
