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

c.execute("""CREATE TABLE IF NOT EXISTS levelscompleted (
          userID INTEGER PRIMARY KEY,
          init BOOLEAN,
          level1 BOOLEAN,
          level2 BOOLEAN,
          level3 BOOLEAN,
          level4 BOOLEAN,
          level5 BOOLEAN,
          level6 BOOLEAN,
          level7 BOOLEAN,
          level8 BOOLEAN,
          level9 BOOLEAN,
          level10 BOOLEAN,
          level11 BOOLEAN,
          level12 BOOLEAN,
          level_enemies BOOLEAN
          )""")
c.execute("""DROP TABLE
          IF EXISTS 
          level_enemies""")
c.execute("""CREATE TABLE
          IF NOT EXISTS
          level_enemies(level integer, enemy varchar, frequency integer)""")
c.execute("""INSERT INTO level_enemies
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
c.execute("""CREATE TABLE IF NOT EXISTS
          skins_purchased(user_id integer,
          Initial BOOLEAN,
          Green BOOLEAN,
          Grey BOOLEAN,
          Orange BOOLEAN,
          Purple BOOLEAN,
          Black BOOLEAN,
          Naked BOOLEAN,
          Gman BOOLEAN,
          selected varchar)""")
c.execute("""CREATE TABLE IF NOT EXISTS skills_purchased (
          user_id INTEGER,
          skill_1 BOOLEAN,
          skill_2 BOOLEAN,
          skill_3 BOOLEAN,
          skill_4 BOOLEAN,
          skill_5 BOOLEAN,
          skill_6 BOOLEAN,
          skill_7 BOOLEAN,
          skill_8 BOOLEAN,
          skill_9 BOOLEAN,
          skill_10 BOOLEAN,
          skill_11 BOOLEAN,
          skill_12 BOOLEAN,
          skill_13 BOOLEAN,
          skill_14 BOOLEAN,
          skill_15 BOOLEAN)""")

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

#Adds new username and relevent information to other tables
def new_username(new_name):
    c.execute("""INSERT INTO users(username,in_use,currency,redeemed)
               VALUES (?,False,0,0)""",(str(new_name),))
    c.execute("""INSERT INTO levelscompleted (userID, init,level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12)
    SELECT 
        userID, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    FROM users
    WHERE username = ?;""", (str(new_name),))
    c.execute("""INSERT INTO skins_purchased(user_id, Initial, Green, Grey, Orange, Purple, Black, Naked, Gman, selected)
              SELECT 
                userID, 1,0,0,0,0,0,0,0,"Initial"
                FROM users
                WHERE username = ?;""", (str(new_name),))
    c.execute("""INSERT INTO skills_purchased(user_id, skill_1, skill_2, skill_3, skill_4, skill_5, skill_6, skill_7, skill_8, skill_9, skill_10, skill_11, skill_12, skill_13, skill_14, skill_15)
              SELECT
              userID , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                FROM users
                WHERE username = ?;""", (str(new_name),))
    conn.commit()

#Deletes user
def delete_user(username):
    c.execute("""DELETE FROM levelscompleted 
              WHERE userID = (SELECT userID FROM users WHERE username = ?)""",(str(username),))
    c.execute("""DELETE FROM users
               WHERE username = ?""",(str(username),))
    c.execute("""DELETE FROM skins_purchased
                WHERE user_id = (SELECT userID FROM users WHERE username = ?)""",(str(username),))
    c.execute("""DELETE FROM skills_purchased
                WHERE user_id = (SELECT userID FROM users WHERE username = ?)""",(str(username),))

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

#Purchase skill
def purchase_skill(skill):
    c.execute(f"""UPDATE skills_purchased
                SET skill_{skill} = 1
                WHERE user_id = (SELECT userID FROM users WHERE in_use = 1)""")
    conn.commit()

#Return skills
def get_skills():
    c.execute("""SELECT skill_1, skill_2, skill_3, skill_4, skill_5, skill_6, skill_7, skill_8, skill_9, skill_10, skill_11, skill_12, skill_13, skill_14, skill_15
                FROM skills_purchased
               WHERE user_id = (SELECT userID FROM users WHERE in_use = 1)""")
    return c.fetchall()[0]
    
#Return skins
def is_skin_puchased(skin):
    c.execute(f"""SELECT {skin} FROM skins_purchased
              WHERE user_id = (SELECT userID FROM users WHERE in_use = 1) """)
    return c.fetchone()[0]

def get_selected_skin():
    c.execute("""SELECT selected FROM skins_purchased
              WHERE user_id = (SELECT userID FROM users WHERE in_use = 1)""")
    return c.fetchone()[0]


#Select/purchase skin
def select_skin(skin,select,purchase):
    if select:
        c.execute("""UPDATE skins_purchased
                  SET selected = ?
                  WHERE user_id = (SELECT userID FROM users WHERE in_use = 1)""",(str(skin),))
    if purchase:
        c.execute(f"""UPDATE skins_purchased
                  SET {skin} = 1
                  WHERE user_id = (SELECT userID FROM users WHERE in_use = 1)""")
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
