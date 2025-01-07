import sqlite3

conn = sqlite3.connect("Gun dude database.db")
c = conn.cursor()

#set up database
c.execute("""CREATE TABLE 
          IF NOT EXISTS 
          enemy_information(enemy_type varchar,
          health integer,
          damage float,
          speed float, 
          is_boss boolean,
          PRIMARY KEY (enemy_type))""")
c.execute("""REPLACE INTO enemy_information
          VALUES("Fly",2,1,1,0),
          ("Trash",5,2,0.6,0),
          ("Thug",5,3,0.6,0),
          ("Ninja",10,2.5,0.9,0),
          ("Robot boss",600,6,1,1),
          ("Zombie",7,4,0.75,0),
          ("Mummy",8,2.5,0.4,0),
          ("UFO",3,3,1,0),
          ("Alien",10,3,0.8,0),
          ("Alien boss",1000,10,1,1),
          ("Evil dude",2000,12,1.5,1),
          ("Demon boss",3000,14,1.2,1)""")
c.execute("""CREATE TABLE 
          IF NOT EXISTS 
          boss_information(boss varchar,
          projectile varchar, 
          shoot_speed integer,
          spawn_time integer,
          PRIMARY KEY (boss))""")
c.execute("""REPLACE INTO boss_information
          VALUES("Robot boss","Missile",100,30),
          ("Alien boss","Fireball",70,50),
          ("Evil dude","Evil bullet",50,30),
          ("Demon boss","Fireball",40,10)""")
c.execute("""CREATE TABLE IF NOT EXISTS 
          users(userID integer primary key autoincrement,
          username varchar,in_use boolean,
          currency integer, 
          redeemed boolean)""")
c.execute("""CREATE TABLE IF NOT EXISTS levelscompleted(userID integer primary key,
          init boolean,
          level1 boolean,
          level2 boolean,
          level3 boolean,
          level4 boolean,
          level5 boolean,
          level6 boolean,
          level7 boolean,
          level8 boolean,
          level9 boolean,
          level10 boolean,
          level11 boolean,
          level12 boolean)""")
c.execute("""CREATE TABLE IF NOT EXISTS """)
c.execute("""DROP TABLE
          IF EXISTS level_enemies""")
c.execute("""CREATE TABLE
          IF NOT EXISTS
          level_enemies(level integer, enemy varchar, frequency integer)""")
c.execute("""REPLACE INTO level_enemies
          VALUES(1,"Fly",1),
          (2,"Fly",3),(2,"Trash",1),
          (3,"Thug",5),(3,"Ninja",1),
          (4,"Thug",2),(4,"Ninja",1),(4,"Robot boss",1),
          (5,"Fly",1),(5,"Trash",1),(5,"Thug",1),
          (6,"Fly",1),(6,"Trash",1),(6,"Zombie",1),
          (7,"Ninja",1),(7,"Mummy",1),
          (8,"Mummy",1),(8,"Zombie",1),
          (9,"UFO",6),(9,"Alien",1),
          (10,"Alien",1),(10,"UFO",1),(10,"Alien boss",1),
          (11,"UFO",1),(11,"Fly",1),(11,"Trash",1),(11,"Thug",1),(11,"Evil dude",1),
          (12,"Zombie",1),(12,"Mummy",1),(12,"Alien",1),(12,"Ninja",1),(12,"Demon boss",1)""")

conn.commit()

#Returns which levels are completed for specific user
def is_complete(user):
    c.execute(f"""SELECT 
              levelscompleted.* 
              FROM levelscompleted
              JOIN users
              ON levelscompleted.userID = users.userID
              WHERE users.username = ?;""",(str(user),))
    conn.commit()
    return c.fetchall()[0]

#Switches a level's state to complete
def complete_level(level,user):
    c.execute(f"""UPDATE levelscompleted 
              SET level{level} = 1 
              WHERE userID = (SELECT userID from users where username = ?)""",(str(user),))
    conn.commit()

#Returns which enemies feature on an inputted level
def get_enemies(level):
    c.execute("""SELECT * 
              FROM enemy_information
              INNER JOIN level_enemies 
              ON level_enemies.enemy = enemy_information.enemy_type AND level_enemies.level = ?""",(str(level),))
    return c.fetchall()

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
              FROM users
              WHERE in_use = 1""")
    return c.fetchall()[0][0]
    
#Adds to the player's currency
def add_currency(amount):
    c.execute(f"""UPDATE users
              SET currency = currency + ?
              WHERE in_use = 1""", (str(amount),))
    conn.commit()

#Returns all usernames 
def return_user_info():
    c.execute("""SELECT username, in_use
              FROM users""")
    return c.fetchall()

#Adds new username
def new_username(new_name):
    c.execute("""INSERT INTO users(username,in_use,currency,redeemed)
               VALUES (?,False,0,0)""",(str(new_name),))
    c.execute("""INSERT INTO levelscompleted (userID, init,level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12)
    SELECT 
        userID, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    FROM users
    WHERE username = ?;""", (str(new_name),))
    conn.commit()

#Deletes user
def delete_user(username):
    c.execute("""DELETE FROM levelscompleted 
              WHERE userID = (SELECT userID FROM users WHERE username = ?)""",(str(username),))
    c.execute("""DELETE FROM users
               WHERE username = ?""",(str(username),))
    c.execute(f"""DROP TABLE {username}skills""")
    c.execute(f"""DROP TABLE {username}skins""")
    conn.commit()

#Choose user
def choose_user(username):
    c.execute("""UPDATE users
              SET in_use = 
              (CASE WHEN username = ? THEN 1 
              ELSE 0 
              END)""",(str(username),))
    conn.commit()

#Return user
def get_user():
    c.execute("""SELECT username 
              FROM users
              WHERE in_use = 1""")
    user = c.fetchone()
    if user is None:
        return 'Select/create a user to play'
    else:
        return user[0]

#Create user table
def create_tables(username):
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
    c.execute("""SELECT username FROM users
              WHERE in_use = 1""")
    user = c.fetchone()[0]
    c.execute(f"""UPDATE {user}skills
              SET purchased = 1
              WHERE skill = ?""",(str(skill),))
    conn.commit()

#Return skills
def get_skills():
    c.execute("""SELECT username FROM users
              WHERE in_use = 1""")
    user = c.fetchone()[0]
    c.execute(f"""SELECT skill FROM {user}skills
              WHERE purchased = 1""")
    return c.fetchall()
    
#Return skins
def is_skin_puchased(skin):
    c.execute("""SELECT username FROM users
              WHERE in_use = 1""")
    user = c.fetchone()[0]
    c.execute(f"""SELECT purchased FROM {user}skins
              WHERE skin = ?""",(str(skin),))
    return c.fetchone()[0]

def get_selected_skin():
    c.execute("""SELECT username FROM users
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
    c.execute("""SELECT username FROM users
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

#redeem discount code
def check_for_redeem(user):
    c.execute("""SELECT redeemed FROM users
              WHERE username = ?""",(str(user),))
    return c.fetchone()[0]

#check if redeemed
def redeem_code(user):
    c.execute("""UPDATE users
              SET redeemed = 1
              WHERE username = ?""",(str(user),))
    conn.commit()

#Closes database
def close():
    conn.close()
